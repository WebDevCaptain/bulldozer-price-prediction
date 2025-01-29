
def turn_object_values_to_categories(df: pd.DataFrame):
    for label, content in df.items():
        if pd.api.types.is_object_dtype(content):
            df[label] = df[label].astype("category")

    return df


def fill(df: pd.DataFrame):
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
