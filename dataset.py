# dataset.py
# This file contains your test questions and the correct/ideal answers.
# Think of this as your "exam paper" that you'll use to grade AI models.

EVAL_DATASET = [
    {
        "id": 1,
        "category": "Finance",
        "question": "What is compound interest?",
        "ideal_answer": "Compound interest is interest calculated on both the initial principal and the accumulated interest from previous periods. It causes investments to grow faster over time because you earn interest on your interest."
    },
    {
        "id": 2,
        "category": "Finance",
        "question": "What is a stock market index?",
        "ideal_answer": "A stock market index tracks the performance of a group of stocks representing a portion of the market. Examples include the S&P 500 which tracks 500 large US companies, and the Dow Jones Industrial Average which tracks 30 major US companies."
    },
    {
        "id": 3,
        "category": "Finance",
        "question": "What is inflation?",
        "ideal_answer": "Inflation is the rate at which the general level of prices for goods and services rises over time, reducing purchasing power. Central banks try to control inflation by adjusting interest rates."
    },
    {
        "id": 4,
        "category": "Finance",
        "question": "What is diversification in investing?",
        "ideal_answer": "Diversification is a risk management strategy that involves spreading investments across different asset classes, sectors, or geographies to reduce exposure to any single investment. The goal is to minimize risk without significantly reducing returns."
    },
    {
        "id": 5,
        "category": "Finance",
        "question": "What is a mutual fund?",
        "ideal_answer": "A mutual fund is a pooled investment vehicle that collects money from many investors and invests it in a diversified portfolio of stocks, bonds, or other securities. It is managed by professional fund managers."
    },
    {
        "id": 6,
        "category": "AI & Tech",
        "question": "What is machine learning?",
        "ideal_answer": "Machine learning is a subset of artificial intelligence where systems learn from data to improve their performance on tasks without being explicitly programmed. It includes supervised, unsupervised, and reinforcement learning."
    },
    {
        "id": 7,
        "category": "AI & Tech",
        "question": "What is overfitting in machine learning?",
        "ideal_answer": "Overfitting occurs when a machine learning model learns the training data too well, including its noise and outliers, causing poor performance on new unseen data. It means the model memorizes rather than generalizes."
    },
    {
        "id": 8,
        "category": "AI & Tech",
        "question": "What is a neural network?",
        "ideal_answer": "A neural network is a computational model inspired by the human brain, consisting of layers of interconnected nodes or neurons. It learns patterns from data by adjusting the weights of connections through a process called backpropagation."
    },
    {
        "id": 9,
        "category": "AI & Tech",
        "question": "What is the difference between AI and machine learning?",
        "ideal_answer": "AI is the broad field of creating machines that can perform tasks requiring human intelligence. Machine learning is a subset of AI that focuses specifically on systems that learn from data. All machine learning is AI, but not all AI is machine learning."
    },
    {
        "id": 10,
        "category": "AI & Tech",
        "question": "What is a large language model (LLM)?",
        "ideal_answer": "A large language model is an AI system trained on vast amounts of text data to understand and generate human language. It uses transformer architecture and can perform tasks like answering questions, writing, summarizing, and coding."
    },
    {
        "id": 11,
        "category": "General Knowledge",
        "question": "What causes climate change?",
        "ideal_answer": "Climate change is primarily caused by human activities that release greenhouse gases like CO2 and methane into the atmosphere. The main sources are burning fossil fuels, deforestation, and industrial processes. These gases trap heat and cause global temperatures to rise."
    },
    {
        "id": 12,
        "category": "General Knowledge",
        "question": "How does the internet work?",
        "ideal_answer": "The internet is a global network of computers that communicate using standardized protocols like TCP/IP. Data is broken into packets, sent through routers and switches across physical infrastructure, and reassembled at the destination."
    },
    {
        "id": 13,
        "category": "General Knowledge",
        "question": "What is DNA?",
        "ideal_answer": "DNA (deoxyribonucleic acid) is a molecule that carries the genetic instructions for the development, functioning, growth, and reproduction of all known living organisms. It is structured as a double helix made of four nucleotide bases."
    },
    {
        "id": 14,
        "category": "General Knowledge",
        "question": "What is the difference between a virus and a bacteria?",
        "ideal_answer": "Bacteria are single-celled living organisms that can reproduce independently and can be treated with antibiotics. Viruses are non-living particles that need a host cell to replicate and cannot be treated with antibiotics — antivirals or vaccines are used instead."
    },
    {
        "id": 15,
        "category": "General Knowledge",
        "question": "What is the speed of light?",
        "ideal_answer": "The speed of light in a vacuum is approximately 299,792 kilometers per second (about 186,000 miles per second). It is denoted by the letter c and is a fundamental constant in physics, playing a key role in Einstein's theory of relativity."
    }
]
