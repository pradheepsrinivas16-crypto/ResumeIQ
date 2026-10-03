import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader
from torch import nn
from sklearn.preprocessing import LabelEncoder
from collections import Counter


# ==========================================
# SETTINGS
# ==========================================

MAX_LENGTH = 300
BATCH_SIZE = 32
EMBEDDING_DIM = 128


# ==========================================
# LOAD DATA
# ==========================================

train_df = pd.read_csv(
    "data/processed/train.csv"
)

validation_df = pd.read_csv(
    "data/processed/validation.csv"
)

test_df = pd.read_csv(
    "data/processed/test.csv"
)


print("Train samples:", len(train_df))
print("Validation samples:", len(validation_df))
print("Test samples:", len(test_df))


# ==========================================
# LABEL ENCODING
# ==========================================

label_encoder = LabelEncoder()

train_labels = label_encoder.fit_transform(
    train_df["Category"]
)

validation_labels = label_encoder.transform(
    validation_df["Category"]
)

test_labels = label_encoder.transform(
    test_df["Category"]
)


print("Number of categories:", len(label_encoder.classes_))


# ==========================================
# SIMPLE TOKENIZER
# ==========================================

def tokenize(text):

    return text.lower().split()


# ==========================================
# BUILD VOCABULARY
# ==========================================

counter = Counter()

for text in train_df["Resume_str"]:

    counter.update(
        tokenize(text)
    )


# Keep most common 20,000 words

MAX_VOCAB_SIZE = 20000

most_common_words = counter.most_common(
    MAX_VOCAB_SIZE
)


word_to_index = {
    "<PAD>": 0,
    "<UNK>": 1
}


for index, (word, _) in enumerate(
    most_common_words,
    start=2
):

    word_to_index[word] = index


print(
    "Vocabulary size:",
    len(word_to_index)
)


# ==========================================
# TEXT ENCODING
# ==========================================

def encode_text(text):

    tokens = tokenize(text)

    token_ids = []

    for token in tokens:

        token_ids.append(
            word_to_index.get(
                token,
                word_to_index["<UNK>"]
            )
        )


    # Truncate

    token_ids = token_ids[:MAX_LENGTH]


    # Padding

    while len(token_ids) < MAX_LENGTH:

        token_ids.append(
            word_to_index["<PAD>"]
        )


    return token_ids


# ==========================================
# DATASET
# ==========================================

class ResumeDataset(Dataset):

    def __init__(
        self,
        dataframe,
        labels
    ):

        self.texts = dataframe[
            "Resume_str"
        ].tolist()

        self.labels = labels


    def __len__(self):

        return len(self.texts)


    def __getitem__(self, index):

        text = encode_text(
            self.texts[index]
        )

        label = self.labels[index]


        return (
            torch.tensor(
                text,
                dtype=torch.long
            ),

            torch.tensor(
                label,
                dtype=torch.long
            )
        )


# ==========================================
# CREATE DATASETS
# ==========================================

train_dataset = ResumeDataset(
    train_df,
    train_labels
)

validation_dataset = ResumeDataset(
    validation_df,
    validation_labels
)

test_dataset = ResumeDataset(
    test_df,
    test_labels
)


# ==========================================
# DATA LOADERS
# ==========================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=BATCH_SIZE
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE
)


# ==========================================
# CHECK DATA
# ==========================================

x, y = next(
    iter(train_loader)
)


print("\n======================================")
print("       CNN DATA PREPARATION")
print("======================================")

print(
    "Input shape:",
    x.shape
)

print(
    "Label shape:",
    y.shape
)

print(
    "First label:",
    y[0].item()
)

print(
    "First category:",
    label_encoder.classes_[y[0].item()]
)

print("======================================")
# ==========================================
# CNN MODEL
# ==========================================

class CNNTextClassifier(nn.Module):

    def __init__(
        self,
        vocab_size,
        embedding_dim,
        num_classes
    ):

        super().__init__()

        # Word embedding
        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
            padding_idx=0
        )

        # CNN layers
        self.conv3 = nn.Conv1d(
            in_channels=embedding_dim,
            out_channels=128,
            kernel_size=3
        )

        self.conv4 = nn.Conv1d(
            in_channels=embedding_dim,
            out_channels=128,
            kernel_size=4
        )

        self.conv5 = nn.Conv1d(
            in_channels=embedding_dim,
            out_channels=128,
            kernel_size=5
        )

        # Classification layer
        self.dropout = nn.Dropout(0.5)

        self.fc = nn.Linear(
            128 * 3,
            num_classes
        )


    def forward(self, x):

        # x:
        # [batch_size, sequence_length]

        x = self.embedding(x)

        # [batch, sequence, embedding]
        x = x.permute(
            0, 2, 1
        )

        # [batch, embedding, sequence]

        x3 = torch.relu(
            self.conv3(x)
        )

        x4 = torch.relu(
            self.conv4(x)
        )

        x5 = torch.relu(
            self.conv5(x)
        )

        # Global max pooling

        x3 = torch.max(
            x3,
            dim=2
        ).values

        x4 = torch.max(
            x4,
            dim=2
        ).values

        x5 = torch.max(
            x5,
            dim=2
        ).values

        # Combine CNN features

        x = torch.cat(
            [x3, x4, x5],
            dim=1
        )

        x = self.dropout(x)

        # Classification

        output = self.fc(x)

        return output


# ==========================================
# CREATE MODEL
# ==========================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

model = CNNTextClassifier(
    vocab_size=len(word_to_index),
    embedding_dim=EMBEDDING_DIM,
    num_classes=len(
        label_encoder.classes_
    )
)

model = model.to(device)


# ==========================================
# MODEL SUMMARY
# ==========================================

print("\n======================================")
print("          CNN MODEL")
print("======================================")

print(model)

print("\nDevice:", device)

print(
    "\nTotal parameters:",
    sum(
        p.numel()
        for p in model.parameters()
    )
)

print("======================================")
# ==========================================
# TRAINING SETTINGS
# ==========================================

EPOCHS = 10
LEARNING_RATE = 0.001

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# ==========================================
# TRAINING FUNCTION
# ==========================================

def train_one_epoch():

    model.train()

    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:

        inputs = inputs.to(device)
        labels = labels.to(device)

        # Clear previous gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)

        # Calculate loss
        loss = criterion(
            outputs,
            labels
        )

        # Backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        total_loss += loss.item()

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    average_loss = (
        total_loss / len(train_loader)
    )

    accuracy = (
        correct / total * 100
    )

    return average_loss, accuracy


# ==========================================
# VALIDATION FUNCTION
# ==========================================

def evaluate():

    model.eval()

    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():

        for inputs, labels in validation_loader:

            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)

            loss = criterion(
                outputs,
                labels
            )

            total_loss += loss.item()

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    average_loss = (
        total_loss / len(validation_loader)
    )

    accuracy = (
        correct / total * 100
    )

    return average_loss, accuracy


# ==========================================
# TRAIN CNN
# ==========================================

print("\n======================================")
print("          CNN TRAINING")
print("======================================")

for epoch in range(EPOCHS):

    train_loss, train_accuracy = (
        train_one_epoch()
    )

    validation_loss, validation_accuracy = (
        evaluate()
    )

    print(
        f"\nEpoch {epoch + 1}/{EPOCHS}"
    )

    print(
        f"Train Loss: {train_loss:.4f}"
    )

    print(
        f"Train Accuracy: "
        f"{train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: "
        f"{validation_loss:.4f}"
    )

    print(
        f"Validation Accuracy: "
        f"{validation_accuracy:.2f}%"
    )


print("\n======================================")
print("       CNN TRAINING COMPLETE")
print("======================================")
from sklearn.metrics import classification_report, accuracy_score

model.eval()

all_predictions = []
all_labels = []

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs = inputs.to(device)

        outputs = model(inputs)
        predictions = torch.argmax(outputs, dim=1)

        all_predictions.extend(predictions.cpu().numpy())
        all_labels.extend(labels.numpy())

test_accuracy = accuracy_score(all_labels, all_predictions)

print("\n======================================")
print("          CNN TEST RESULTS")
print("======================================")
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

print("======================================")