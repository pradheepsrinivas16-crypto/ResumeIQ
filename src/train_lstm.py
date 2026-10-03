import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from sklearn.preprocessing import LabelEncoder
from collections import Counter

MAX_LENGTH = 300
BATCH_SIZE = 32
EMBEDDING_DIM = 128

# Load datasets
train_df = pd.read_csv("data/processed/train.csv")
validation_df = pd.read_csv("data/processed/validation.csv")
test_df = pd.read_csv("data/processed/test.csv")

print("Train samples:", len(train_df))
print("Validation samples:", len(validation_df))
print("Test samples:", len(test_df))

# Encode categories
label_encoder = LabelEncoder()

train_labels = label_encoder.fit_transform(train_df["Category"])
validation_labels = label_encoder.transform(validation_df["Category"])
test_labels = label_encoder.transform(test_df["Category"])

print("Number of categories:", len(label_encoder.classes_))


# Tokenization
def tokenize(text):
    return text.lower().split()


# Build vocabulary using TRAIN data only
counter = Counter()

for text in train_df["Resume_str"]:
    counter.update(tokenize(text))

MAX_VOCAB_SIZE = 20000

most_common_words = counter.most_common(MAX_VOCAB_SIZE)

word_to_index = {
    "<PAD>": 0,
    "<UNK>": 1
}

for index, (word, _) in enumerate(most_common_words, start=2):
    word_to_index[word] = index

print("Vocabulary size:", len(word_to_index))


# Convert text into numbers
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

    # Limit length
    token_ids = token_ids[:MAX_LENGTH]

    # Padding
    while len(token_ids) < MAX_LENGTH:
        token_ids.append(word_to_index["<PAD>"])

    return token_ids


# Dataset
class ResumeDataset(Dataset):

    def __init__(self, dataframe, labels):

        self.texts = dataframe["Resume_str"].tolist()
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):

        text = encode_text(self.texts[index])
        label = self.labels[index]

        return (
            torch.tensor(text, dtype=torch.long),
            torch.tensor(label, dtype=torch.long)
        )


# Create datasets
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


# Create DataLoaders
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


# Check data
x, y = next(iter(train_loader))

print("\n======================================")
print("       LSTM DATA PREPARATION")
print("======================================")

print("Input shape:", x.shape)
print("Label shape:", y.shape)

print("First label:", y[0].item())

print(
    "First category:",
    label_encoder.classes_[y[0].item()]
)

print("======================================")
class LSTMTextClassifier(nn.Module):

    def __init__(
        self,
        vocab_size,
        embedding_dim,
        hidden_dim,
        num_classes
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            embedding_dim,
            padding_idx=0
        )

        self.lstm = nn.LSTM(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            batch_first=True
        )

        self.dropout = nn.Dropout(0.5)

        self.fc = nn.Linear(
            hidden_dim,
            num_classes
        )

    def forward(self, x):

        x = self.embedding(x)

        output, (hidden, cell) = self.lstm(x)

        hidden = hidden[-1]

        hidden = self.dropout(hidden)

        output = self.fc(hidden)

        return output


# Device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


# Create model
HIDDEN_DIM = 128

model = LSTMTextClassifier(
    vocab_size=len(word_to_index),
    embedding_dim=EMBEDDING_DIM,
    hidden_dim=HIDDEN_DIM,
    num_classes=len(label_encoder.classes_)
)

model = model.to(device)


print("\n======================================")
print("          LSTM MODEL")
print("======================================")

print(model)

print("\nDevice:", device)

print(
    "\nTotal parameters:",
    sum(p.numel() for p in model.parameters())
)

print("======================================")
EPOCHS = 10
LEARNING_RATE = 0.001

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


def train_one_epoch():

    model.train()

    total_loss = 0
    correct = 0
    total = 0

    for inputs, labels in train_loader:

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = criterion(outputs, labels)

        loss.backward()

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

    average_loss = total_loss / len(train_loader)

    accuracy = correct / total * 100

    return average_loss, accuracy


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

            loss = criterion(outputs, labels)

            total_loss += loss.item()

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    average_loss = total_loss / len(validation_loader)

    accuracy = correct / total * 100

    return average_loss, accuracy


print("\n======================================")
print("          LSTM TRAINING")
print("======================================")


for epoch in range(EPOCHS):

    train_loss, train_accuracy = train_one_epoch()

    validation_loss, validation_accuracy = evaluate()

    print(f"\nEpoch {epoch + 1}/{EPOCHS}")

    print(
        f"Train Loss: {train_loss:.4f}"
    )

    print(
        f"Train Accuracy: {train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: {validation_loss:.4f}"
    )

    print(
        f"Validation Accuracy: {validation_accuracy:.2f}%"
    )


print("\n======================================")
print("       LSTM TRAINING COMPLETE")
print("======================================")
from sklearn.metrics import classification_report, accuracy_score

model.eval()

all_predictions = []
all_labels = []

with torch.no_grad():

    for inputs, labels in test_loader:

        inputs = inputs.to(device)

        outputs = model(inputs)

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.numpy()
        )


test_accuracy = accuracy_score(
    all_labels,
    all_predictions
)

print("\n======================================")
print("          LSTM TEST RESULTS")
print("======================================")

print(
    f"Test Accuracy: {test_accuracy * 100:.2f}%"
)

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