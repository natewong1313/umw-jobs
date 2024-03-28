# print(calculate_distance(parsed_jobs[0]["locations"][0], user_info["location"]))

# encoded_experiences = job_df["experience_levels"].str.get_dummies(sep=",")
# job_df = pd.concat([job_df, encoded_experiences], axis=1)
# job_df.drop("experience_levels", axis=1, inplace=True)

# print(parsed_jobs[0])

# X_test = pd.DataFrame([{"Gr Liv Area": 1800, "Bedroom AbvGr": 3, "Full Bath": 2}])

# X_train = job_df[["skills"]]
# y_train = job_df["title"]

# scaler = StandardScaler()
# scaler.fit(X_train)
# X_train_scaled = scaler.transform(X_train)


# job_df["Junior"] = job_df["experience_levels"].apply(
#     lambda x: 1 if "Junior" in x else 0
# )
# job_df["Mid Level"] = job_df["experience_levels"].apply(
#     lambda x: 1 if "Mid Level" in x else 0
# )
# job_df["Senior"] = job_df["experience_levels"].apply(
#     lambda x: 1 if "Senior" in x else 0
# )

# X_test = pd.DataFrame({"experience_levels": ["junior"]})

# X_train = job_df[["Junior", "Mid Level", "Senior"]]
# y_train = job_df["title"]

# from sklearn.ensemble import RandomForestClassifier

# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# y_pred = model.predict(X_test)
# print(y_pred)


# col_transformer = make_column_transformer(
#     (
#         CountVectorizer(tokenizer=lambda x: x.split(","), lowercase=False),
#         ["experience_levels"],
#     ),
#     remainder="drop",
# )

# pipeline = make_pipeline(col_transformer, KNeighborsClassifier(n_neighbors=3))

# X_train = job_df[["experience_levels"]]
# y_train = job_df["title"]
# pipeline.fit(X_train, y_train)
# print(pipeline.predict(X=X_test))

# pipeline = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=10))

# job_df["skills"] = job_df["skills"].apply(lambda x: x.split(","))

# tfidf = TfidfVectorizer()
# skills_tfidf = tfidf.fit_transform(job_df["skills"].apply(lambda x: " ".join(x)))

# X = pd.concat(
#     [
#         pd.DataFrame(skills_tfidf.toarray(), columns=tfidf.get_feature_names()),
#         job_df[["Junior", "Mid Level", "Senior"]],
#     ],
#     axis=1,
# )
# y = job_df["title"]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Evaluate the model
# y_pred = model.predict(X_test)
# # accuracy = accuracy_score(y_test, y_pred)
# # print("Accuracy:", accuracy)
