
def turn_object_values_to_categories(df: pd.DataFrame):
    for label, content in df.items():
        if pd.api.types.is_object_dtype(content):
            df[label] = df[label].astype("category")

    return df


def fill_missing_numeric_values(df: pd.DataFrame):
    """ Fill missing numeric values with the median of the target column """
    for label, content in df.items():
        if pd.api.types.is_numeric_dtype(content):
            if pd.isnull(content).sum():

                # Add a binary column which tells if the data was missing our not
                df[label + "_is_missing"] = pd.isnull(content).astype(
                    int
                )  # this will add a 0 or 1 value to rows with missing values (e.g. 0 = not missing, 1 = missing)

                # Fill missing numeric values with median since it's more robust than the mean
                df[label] = content.fillna(content.median())

    return df


def convert_object_values_to_categories_and_fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Create a dictionary to store column to category values (e.g. we turn our category types into numbers but we keep a record so we can go back)
    column_to_category_dict = {}

    # 2. Turn categorical variables into numbers
    for label, content in df.items():

        # 3. Check columns which *aren't* numeric
        if not pd.api.types.is_numeric_dtype(content):

            # 4. Add binary column to inidicate whether sample had missing value
            df[label + "_is_missing"] = pd.isnull(content).astype(int)

            # 5. Ensure content is categorical and get its category codes
            content_categories = pd.Categorical(content)
            content_category_codes = (
                content_categories.codes + 1
            )  # prevents -1 (the default for NaN values) from being used for missing values (we'll treat missing values as 0)

            # 6. Add column key to dictionary with code: category mapping per column
            column_to_category_dict[label] = dict(
                zip(content_category_codes, content_categories)
            )

            # 7. Set the column to the numerical values (the category code value)
            df[label] = content_category_codes

    return df
