import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('eurojackpot_results.csv')

# Check the basic statistics of the dataset
print(df.describe())

# Check the distribution of the main numbers
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='main_numbers', bins=50)
plt.xlabel('Main Numbers')
plt.ylabel('Frequency')
plt.title('Distribution of Main Numbers')
plt.show()

# Check the distribution of the additional numbers
plt.figure(figsize=(8,6))
sns.histplot(data=df, x='add_numbers', bins=12)
plt.xlabel('Additional Numbers')
plt.ylabel('Frequency')
plt.title('Distribution of Additional Numbers')
plt.show()

# Check the correlation between the main numbers, additional numbers, and predicted data
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Check the relationship between the predicted data and main numbers, additional numbers
sns.pairplot(data=df, y_vars=['predicted_data'], x_vars=['main_numbers', 'add_numbers'])
plt.show()