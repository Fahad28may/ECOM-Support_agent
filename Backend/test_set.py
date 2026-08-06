# Gold-standard evaluation set.
# Each item: the question, what the agent SHOULD do, and (for answerable
# ones) a keyword we expect in a correct answer.
#
# expected_behavior is either "answer" or "refuse".
# expected_keyword is the fact a correct answer must contain (None for refusals).

TEST_SET = [
    # --- Should ANSWER (data clearly covers these) ---
    {"question": "How long does delivery take to Lahore?", "expected_behavior": "answer", "expected_keyword": "1-2"},
    {"question": "What is your return window?", "expected_behavior": "answer", "expected_keyword": "30"},
    {"question": "Is cash on delivery available?", "expected_behavior": "answer", "expected_keyword": "cash"},
    {"question": "How much is the Heritage Wool Shawl?", "expected_behavior": "answer", "expected_keyword": "6200"},
    {"question": "What fabric is the Aurora Kurta made of?", "expected_behavior": "answer", "expected_keyword": "linen"},
    {"question": "What colors does the Coastal Denim Jacket come in?", "expected_behavior": "answer", "expected_keyword": "indigo"},
    {"question": "Do you offer free shipping?", "expected_behavior": "answer", "expected_keyword": "5000"},
    {"question": "Can I return a final sale item?", "expected_behavior": "answer", "expected_keyword": "cannot"},

    # --- Should REFUSE (data does NOT cover these) ---
    {"question": "Do you offer gift wrapping?", "expected_behavior": "refuse", "expected_keyword": None},
    {"question": "Do you have a physical store I can visit?", "expected_behavior": "refuse", "expected_keyword": None},
    {"question": "What is your phone number?", "expected_behavior": "refuse", "expected_keyword": None},
    {"question": "Do you ship internationally to Dubai?", "expected_behavior": "refuse", "expected_keyword": None},
    {"question": "Can I pay with cryptocurrency?", "expected_behavior": "refuse", "expected_keyword": None},
    {"question": "Do you have a loyalty rewards program?", "expected_behavior": "refuse", "expected_keyword": None},

    # --- Edge cases (harder — these reveal real weaknesses) ---
    {"question": "I want something in dark colors, what do you have?", "expected_behavior": "answer", "expected_keyword": "black"},
    {"question": "What's your cheapest product?", "expected_behavior": "answer", "expected_keyword": "1500"},
]

