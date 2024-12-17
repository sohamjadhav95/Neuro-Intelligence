from sklearn.utils import resample
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

# Apply SMOTE to minority classes
X_train_upsampled, y_train_upsampled = SMOTE.fit_resample(X_train_embeddings, y_train_argument)

# Apply Downsampling to the upsampled dataset
train_data = pd.DataFrame(X_train_upsampled)
train_data['label'] = y_train_upsampled

majority_class = train_data[train_data['label'] == 'majority_class_label']
minority_class = train_data[train_data['label'] == 'minority_class_label']

# Downsample majority class
majority_downsampled = resample(
    majority_class,
    replace=False,
    n_samples=len(minority_class),
    random_state=42
)

# Combine into a balanced dataset
balanced_data = pd.concat([majority_downsampled, minority_class])
X_train_balanced = balanced_data.drop(columns=['label']).values
y_train_balanced = balanced_data['label'].values
