# ============================================
# PANDAS CHEATSHEET — Shruti Rajani
# ============================================
# Personal reference built while learning data analytics
# Use this as a reference for every future project


# ============================================
# 1. IMPORTING AND LOADING
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
df = pd.read_csv('filename.csv')
df = pd.read_csv('filename.csv', encoding='latin1')  # if normal load fails

# Save DataFrame to CSV
df.to_csv('output.csv', index=False)  # index=False avoids saving row numbers


# ============================================
# 2. FIRST LOOK AT DATA
# ============================================

df.head()           # first 5 rows
df.tail()           # last 5 rows
df.shape            # (rows, columns)
df.columns          # all column names
df.dtypes           # data type of each column
df.info()           # full overview — types + missing counts
df.describe()       # statistics — mean, min, max, std for number columns


# ============================================
# 3. SELECTING DATA
# ============================================

df['Sales']                          # one column
df[['Sales', 'Profit', 'Region']]    # multiple columns
df.iloc[0]                           # first row by position
df.iloc[0:5]                         # first 5 rows by position
df.loc[0, 'Sales']                   # specific row and column by label


# ============================================
# 4. FILTERING DATA
# ============================================

# Single condition
df[df['Sales'] > 1000]
df[df['Region'] == 'West']
df[df['Profit'] < 0]

# Multiple conditions — use & for AND, | for OR
df[(df['Category'] == 'Furniture') & (df['Profit'] < 0)]
df[(df['Region'] == 'West') | (df['Region'] == 'East')]

# COMMON MISTAKE — never use list in condition
# WRONG: df[df['Category'] == ['Furniture']]
# RIGHT: df[df['Category'] == 'Furniture']


# ============================================
# 5. GROUPBY AND AGGREGATION
# ============================================

df.groupby('Region')['Sales'].sum()       # total sales per region
df.groupby('Region')['Sales'].mean()      # average sales per region
df.groupby('Region')['Sales'].count()     # count of orders per region
df.groupby('Region')['Sales'].max()       # highest sale per region

# Group by multiple columns
df.groupby(['Region', 'Category'])['Sales'].sum()

# Reset index after groupby (needed for seaborn charts)
df.groupby('Region')['Sales'].sum().reset_index()


# ============================================
# 6. SORTING
# ============================================

df.sort_values('Sales')                        # lowest to highest
df.sort_values('Sales', ascending=False)       # highest to lowest
df.sort_values('Sales', ascending=False).head(10)  # top 10


# ============================================
# 7. TOP N AND BOTTOM N
# ============================================

df.nlargest(5, 'Sales')     # top 5 rows by Sales
df.nsmallest(5, 'Profit')   # bottom 5 rows by Profit

# On a grouped series
df.groupby('State')['Sales'].sum().nlargest(10)   # top 10 states by sales


# ============================================
# 8. VALUE COUNTS
# ============================================

df['Region'].value_counts()          # count of each region, sorted
df['Category'].value_counts()        # count of each category
df['City'].value_counts().head(10)   # top 10 cities by order count


# ============================================
# 9. MISSING VALUES
# ============================================

df.isnull().sum()                    # count missing per column
df.isnull().sum() / len(df) * 100   # missing percentage per column

# Fill missing values
df['Sales'].fillna(df['Sales'].median())    # fill numbers with median
df['Sales'].fillna(df['Sales'].mean())      # fill numbers with mean
df['Region'].fillna(df['Region'].mode()[0]) # fill text with most common value

# Drop rows with missing values
df.dropna()                          # drop any row with any missing value
df.dropna(subset=['Customer Name'])  # drop only where Customer Name is missing

# RULE:
# Missing numbers → fill with median (if outliers exist) or mean (if clean)
# Missing text/categories → fill with mode
# Missing IDs or names → drop those rows


# ============================================
# 10. DUPLICATES
# ============================================

df.duplicated().sum()    # count duplicate rows
df.drop_duplicates()     # remove duplicate rows

# RULE: Always remove duplicates BEFORE filling missing values


# ============================================
# 11. OUTLIERS — IQR METHOD
# ============================================

Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)
IQR = Q3 - Q1
upper_limit = Q3 + 1.5 * IQR
lower_limit = Q1 - 1.5 * IQR

# Find outliers
df[df['Sales'] > upper_limit]

# Cap outliers (keep row but fix the value)
df['Sales'] = df['Sales'].clip(upper=upper_limit)

# RULE: Cap outliers instead of dropping when the row itself is valid


# ============================================
# 12. USEFUL ONE-LINERS
# ============================================

df['Order ID'].nunique()              # count unique values
df['Sales'].sum()                     # total
df['Sales'].mean()                    # average
df['Sales'].median()                  # middle value
df['Sales'].max()                     # highest value
df['Sales'].min()                     # lowest value

# Profit margin
profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100


# ============================================
# 13. MATPLOTLIB CHARTS
# ============================================

# Bar chart
plt.figure(figsize=(8, 5))
plt.bar(x_values, y_values, color='steelblue')
plt.title('Chart Title')
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.tight_layout()
plt.savefig('chart.png')   # save before show
plt.show()

# Horizontal bar chart (better for many categories)
plt.barh(y_values, x_values, color='steelblue')

# Histogram (distribution of one column)
plt.hist(df['Sales'], bins=50, color='coral', edgecolor='white')

# Line at zero (useful for profit charts)
plt.axvline(x=0, color='black', linewidth=0.8)   # vertical line
plt.axhline(y=0, color='red', linewidth=0.8)     # horizontal line

# Two charts side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(data1, bins=50, color='coral')
axes[1].hist(data2, bins=50, color='steelblue')


# ============================================
# 14. SEABORN CHARTS
# ============================================

# Bar chart (needs DataFrame with reset_index)
data = df.groupby('Region')['Sales'].sum().reset_index()
sns.barplot(data=data, x='Region', y='Sales',
            hue='Region', palette='Blues_d', legend=False)

# Scatter plot (relationship between two columns)
sns.scatterplot(data=df, x='Discount', y='Profit', alpha=0.4)

# Color palettes: Blues_d, Greens_r, Reds_r, coolwarm, Set2


# ============================================
# 15. LIST COMPREHENSION IN CHARTS
# ============================================

# Color bars based on value (red if negative, blue if positive)
colors = ['red' if x < 0 else 'steelblue' for x in values]
plt.bar(labels, values, color=colors)
