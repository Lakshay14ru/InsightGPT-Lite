import re


def detect_groupwise_question(question, df):
    """Detect group-wise questions using the uploaded dataset's columns."""
    import re

    if df is None or df.empty:
        return {
            "is_groupwise": False,
            "group_column": None,
            "value_column": None
        }

    def normalize(value):
        return re.sub(
            r"[^a-z0-9]+",
            " ",
            str(value).lower()
        ).strip()

    q = normalize(question)

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Detect the grouping column from the actual dataset.
    group_candidates = []

    for column in categorical_columns:
        name = normalize(column)

        if name and re.search(
            r"\b" + re.escape(name) + r"\b", q
        ):
            group_candidates.append(column)

    # Common alternatives, matched to columns that actually exist.
    aliases = {
        "gender": ["sex", "gender"],
        "sex": ["sex", "gender"],
        "school": ["school"],
        "class": ["class", "pclass"],
        "department": ["department", "dept"]
    }

    if not group_candidates:
        for keyword, possible_names in aliases.items():
            if re.search(r"\b" + keyword + r"\b", q):
                for column in categorical_columns:
                    if normalize(column) in possible_names:
                        group_candidates.append(column)

                if group_candidates:
                    break

    group_column = (
        group_candidates[0]
        if len(group_candidates) == 1
        else None
    )

    # Detect the numerical column explicitly mentioned in the question.
    value_candidates = []

    for column in numerical_columns:
        name = normalize(column)

        if name and re.search(
            r"\b" + re.escape(name) + r"\b", q
        ):
            value_candidates.append(column)

    # Grade-related wording refers to G3 when that column exists.
    if not value_candidates and any(
        term in q.split()
        for term in ["grade", "grades", "score", "scores", "marks"]
    ):
        for column in numerical_columns:
            if normalize(column) == "g3":
                value_candidates.append(column)
                break

    # Resolve common numerical-column aliases.
    if not value_candidates:
        value_aliases = {
            "age": ["age"],
            "salary": ["salary", "income", "wage"],
            "fare": ["fare", "price"]
        }

        for keyword, possible_names in value_aliases.items():
            if re.search(r"\b" + keyword + r"\b", q):
                for column in numerical_columns:
                    if normalize(column) in possible_names:
                        value_candidates.append(column)

                if value_candidates:
                    break

    value_column = (
        value_candidates[0]
        if len(value_candidates) == 1
        else None
    )

    groupwise_keywords = [
        "by", "each", "per", "among", "compare",
        "group", "highest", "lowest"
    ]

    is_groupwise = (
        group_column is not None
        and value_column is not None
        and any(
            re.search(r"\b" + re.escape(word) + r"\b", q)
            for word in groupwise_keywords
        )
    )

    return {
        "is_groupwise": is_groupwise,
        "group_column": group_column,
        "value_column": value_column
    }

# ============================================
# SURVIVAL QUESTION DETECTION
# ============================================

def detect_survival_question(question, df):
    """
    Detect whether the user is asking about
    survival rate by a particular group.
    """

    question = question.lower().strip()

    if "Survived" not in df.columns:
        return {
            "is_survival": False,
            "group_column": None
        }

    survival_keywords = [
        "survival rate",
        "survival percentage",
        "percentage survived",
        "survival by",
        "survived by",
        "who survived",
        "highest survival",
        "lowest survival",
        "survival"
    ]

    is_survival_question = any(
        keyword in question
        for keyword in survival_keywords
    )

    if not is_survival_question:
        return {
            "is_survival": False,
            "group_column": None
        }

    # ----------------------------------------
    # Detect grouping column
    # ----------------------------------------

    group_column = None

    if (
        "class" in question
        or "pclass" in question
    ):

        if "Pclass" in df.columns:
            group_column = "Pclass"

    elif (
        "gender" in question
        or "sex" in question
    ):

        if "Sex" in df.columns:
            group_column = "Sex"

    elif (
        "embarked" in question
        or "port" in question
    ):

        if "Embarked" in df.columns:
            group_column = "Embarked"

    return {
        "is_survival": (
            group_column is not None
        ),
        "group_column": group_column
    }