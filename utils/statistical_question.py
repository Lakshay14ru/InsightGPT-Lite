import re


def detect_groupwise_question(question, df):
    """
    Detect whether a question is asking for
    group-wise statistical analysis.
    """

    question = question.lower().strip()

    group_column = None
    value_column = None

    # ============================================
    # GROUP COLUMN DETECTION
    # ============================================

    group_mapping = {
    "class": "Pclass",
    "pclass": "Pclass",
    "passenger class": "Pclass",

    "gender": "Sex",
    "sex": "Sex",

    "embarked": "Embarked",
    "port": "Embarked",

    "survival": "Survived"
}

    for keyword, column in group_mapping.items():

        if (
            keyword in question
            and column in df.columns
        ):
            group_column = column
            break

    # ============================================
    # VALUE COLUMN DETECTION
    # ============================================

    value_mapping = {
        "fare": "Fare",
        "age": "Age",
        "survival": "Survived",
        "siblings": "SibSp",
        "sibsp": "SibSp",
        "parents": "Parch",
        "children": "Parch",
        "parch": "Parch"
    }

    for keyword, column in value_mapping.items():

        if (
            keyword in question
            and column in df.columns
        ):
            value_column = column
            break

    # ============================================
    # CHECK FOR GROUPWISE INTENT
    # ============================================

    groupwise_keywords = [
        "by",
        "each",
        "per",
        "for each",
        "highest average",
        "lowest average",
        "average for",
        "average by",
        "mean by",
        "compare"
    ]

    is_groupwise = any(
        keyword in question
        for keyword in groupwise_keywords
    )

    if (
        is_groupwise
        and group_column
        and value_column
    ):

        return {
            "is_groupwise": True,
            "group_column": group_column,
            "value_column": value_column
        }

    return {
        "is_groupwise": False,
        "group_column": None,
        "value_column": None
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