def classify_question(question):

    question = question.lower().strip()

    # ============================================
    # STATISTICAL KEYWORDS
    # ============================================

    statistical_keywords = [

        # General statistics
        "average",
        "mean",
        "median",
        "mode",
        "minimum",
        "maximum",
        "min",
        "max",
        "sum",
        "total",
        "count",
        "percentage",
        "percent",
        "distribution",
        "standard deviation",
        "variance",

        # Missing values
        "missing",
        "null",
        "empty",
        "missing values",
        "missing data",

        # Duplicates
        "duplicate",
        "duplicates",
        "repeated records",
        "repeated rows",

        # Outliers
        "outlier",
        "outliers",
        "unusual values",
        "abnormal values",
        "extreme values",

        # Correlation
        "correlation",
        "correlated",
        "relationship between",
        "strongest relationship",
        "highest correlation",

        # Dataset structure
        "how many rows",
        "how many columns",
        "number of rows",
        "number of columns",
        "data types",
        "numerical columns",
        "categorical columns"
    ]

    # ============================================
    # RAG / CONTEXT KEYWORDS
    # ============================================

    rag_keywords = [

        "tell me about",
        "describe",
        "explain the dataset",
        "what is this dataset",
        "what does this dataset",
        "information about",
        "details about",
        "dataset contains",
        "what kind of data",
        "passengers",
        "records",
        "entries",
        "examples",
        "show me",
        "which passengers",
        "who"
    ]

    # ============================================
    # CHECK STATISTICAL MATCH
    # ============================================

    statistical_match = any(
        keyword in question
        for keyword in statistical_keywords
    )

    # ============================================
    # CHECK RAG MATCH
    # ============================================

    rag_match = any(
        keyword in question
        for keyword in rag_keywords
    )

    # ============================================
    # QUESTION ROUTING
    # ============================================

    if statistical_match and rag_match:

        return "both"

    elif statistical_match:

        return "statistical"

    elif rag_match:

        return "rag"

    else:

        # Unknown/general questions
        # use both approaches

        return "both"