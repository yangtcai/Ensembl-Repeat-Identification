# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import json
import pathlib

# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from utils import hits_column_dtypes, hits_to_dataframe

# %%
figsize = (16, 9)

# %%
data_directory = pathlib.Path("../data")

annotations_directory = data_directory / "annotations"

# %% [markdown]
# ## repeat annotations

# %%
annotations_path = annotations_directory / "hg38.hits"

repeats = hits_to_dataframe(annotations_path)

# %%
repeats.head()

# %%
# show random sample of items
num_items = 10
random_seed = 5
repeats.sample(num_items, random_state=random_seed).sort_index()

# %%
# concise summary of dataframe
repeats.info()

# %%
# number of distinct elements
repeats.nunique()

# %% [markdown]
# ### value counts

# %%
categorical_variables = {
    "seq_name",
    "family_acc",
    "family_name",
    "strand",
}

# %%
for column in categorical_variables:
    column_value_counts = repeats[column].value_counts()
    print(f"{column=}\n", column_value_counts, "\n")
    column_value_counts[:30]
    column_value_counts[:30].plot(kind="bar", figsize=figsize)
    plt.show()

# %% [markdown] tags=[]
# ### repeats length

# %%
repeats["ali_length"] = abs(repeats["ali-en"] - repeats["ali-st"]) + 1

# %%
repeats.head()

# %%
repeats["ali_length"].value_counts()

# %%
repeats.loc[repeats["ali_length"].sort_values().index][-10:]

# %%
ali_length_mean = repeats["ali_length"].mean()
ali_length_median = repeats["ali_length"].median()
ali_length_std = repeats["ali_length"].std()

print(
    f"ali_length mean: {ali_length_mean:.2f}, median: {ali_length_median:.2f}, standard deviation: {ali_length_std:.2f}"
)

# %%
figure = plt.figure()
ax = repeats["ali_length"].hist(figsize=figsize, bins=256)
ax.axvline(x=ali_length_mean, color="black", linewidth=1)
for count in range(1, 3 + 1):
    x = round(ali_length_mean + count * ali_length_std)
    ax.axvline(x=x, color="red", linewidth=1)
ax.set(xlabel="ali_length", ylabel="number of repeats")
figure.add_axes(ax)

# %%

# %%

# %%

# %% [markdown]
# ## repeat families

# %%
from pprint import pp as pprint


repeat_families_path = annotations_directory / "repeat_families.json"

# load repeat families
with open(repeat_families_path) as json_file:
    families_dict = json.load(json_file)

# %%
counter = 0
for accession, dictionary in families_dict.items():
    pprint(dictionary)
    counter += 1
    if counter == 3:
        break
    print()

# %%

# %%
families = pd.DataFrame.from_records(
    repeat_family for accession, repeat_family in families_dict.items()
)

# %%
families.head()

# %%
# show random sample of items
num_items = 10
random_seed = 5
families.sample(num_items, random_state=random_seed).sort_index()

# %%
# concise summary of dataframe
families.info()

# %%
families = families.drop("clades", axis=1)

# %%
# number of distinct elements
families.nunique()

# %% [markdown]
# ### value counts

# %%
categorical_variables = {
    "repeat_type_name",
    "repeat_subtype_name",
}

# %%
for column in categorical_variables:
    column_value_counts = families[column].value_counts()
    print(f"{column=}\n", column_value_counts, "\n")
    column_value_counts[:30]
    column_value_counts[:30].plot(kind="bar", figsize=figsize)
    plt.show()

# %%
type_subtype_value_counts = families[
    ["repeat_type_name", "repeat_subtype_name"]
].value_counts()
print(f"{column=}\n", type_subtype_value_counts, "\n")
type_subtype_value_counts[:40]
type_subtype_value_counts[:40].plot(kind="bar", figsize=figsize)
plt.show()

# %%

# %%

# %%

# %% [markdown]
# ## save repeat type and subtype names in repeats DataFrame

# %%
repeats["repeat_type_name"] = (
    repeats[~repeats["family_acc"].map(families_dict).isna()]["family_acc"]
    .map(families_dict)
    .apply(lambda x: x.get("repeat_type_name"))
)

# %%
repeats["repeat_subtype_name"] = (
    repeats[~repeats["family_acc"].map(families_dict).isna()]["family_acc"]
    .map(families_dict)
    .apply(lambda x: x.get("repeat_subtype_name"))
)

# %%
repeats

# %%

# %% [markdown]
# ## select a repeat type

# %%
repeat_type_name = "LTR"
repeats_type = repeats[repeats["repeat_type_name"] == repeat_type_name]
families_type = families[families["repeat_type_name"] == repeat_type_name]

# %%
repeats_type.sample(10, random_state=5).sort_index()

# %%
families_type.sample(10, random_state=5).sort_index()

# %%
sorted(families_type["classification"].unique())

# %%

# %%
repeats_type_ali_length_mean = repeats_type["ali_length"].mean()
repeats_type_ali_length_median = repeats_type["ali_length"].median()
repeats_type_ali_length_std = repeats_type["ali_length"].std()

print(
    f"ali_length mean: {repeats_type_ali_length_mean:.2f}, median: {repeats_type_ali_length_median:.2f}, standard deviation: {repeats_type_ali_length_std:.2f}"
)

# %%
figure = plt.figure()
ax = repeats_type["ali_length"].hist(figsize=figsize, bins=256)
ax.axvline(x=ali_length_mean, color="black", linewidth=1)
for count in range(1, 3 + 1):
    x = round(repeats_type_ali_length_mean + count * repeats_type_ali_length_std)
    ax.axvline(x=x, color="red", linewidth=1)
ax.set(xlabel="ali_length", ylabel="number of repeats")
figure.add_axes(ax)

# %%
