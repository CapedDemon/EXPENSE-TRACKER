import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expense-tracker",
    version="10.0",
    author="Shreejan Dolai",
    author_email="dolaishreejan@gmail.com",
    description="Expense Tracker is a very good tool to keep track of your expenseditures and the total money you saved.🤑🤑",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CapedDemon/EXPENSE-TRACKER",
    project_urls={
        "Bug Tracker": "https://github.com/CapedDemon/EXPENSE-TRACKER/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    keywords=['expense', 'tracker',
              'money', 'py', 'expense tracker', 'expense-tracker', 'money tracker', 'money-tracker'],
    install_requires=[
        'matplotlib',
        'requests',
        'flask',
        'bcrypt'
    ],
    entry_points={
        'console_scripts': [
            'expense-tracker = expense_tracker.expensetracker:main',
        ],
    }
)
