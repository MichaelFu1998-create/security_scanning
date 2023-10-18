def fit(self, X, y):
        """Fit KimCNNClassifier according to X, y

        Parameters
        ----------
        X : list of string
            each item is a raw text
        y : list of string
            each item is a label
        """
        ####################
        # Data Loader
        ####################
        word_vector_transformer = WordVectorTransformer(padding='max')
        X = word_vector_transformer.fit_transform(X)
        X = LongTensor(X)
        self.word_vector_transformer = word_vector_transformer

        y_transformer = LabelEncoder()
        y = y_transformer.fit_transform(y)
        y = torch.from_numpy(y)
        self.y_transformer = y_transformer

        dataset = CategorizedDataset(X, y)
        dataloader = DataLoader(dataset,
                                batch_size=self.batch_size,
                                shuffle=True,
                                num_workers=4)

        ####################
        # Model
        ####################
        KERNEL_SIZES = self.kernel_sizes
        NUM_KERNEL = self.num_kernel
        EMBEDDING_DIM = self.embedding_dim

        model = TextCNN(
            vocab_size=word_vector_transformer.get_vocab_size(),
            embedding_dim=EMBEDDING_DIM,
            output_size=len(self.y_transformer.classes_),
            kernel_sizes=KERNEL_SIZES,
            num_kernel=NUM_KERNEL)
        if USE_CUDA:
            model = model.cuda()

        ####################
        # Train
        ####################
        EPOCH = self.epoch
        LR = self.lr

        loss_function = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LR)

        for epoch in range(EPOCH):
            losses = []
            for i, data in enumerate(dataloader):
                X, y = data
                X, y = Variable(X), Variable(y)

                optimizer.zero_grad()
                model.train()
                output = model(X)

                loss = loss_function(output, y)
                losses.append(loss.data.tolist()[0])
                loss.backward()

                optimizer.step()

                if i % 100 == 0:
                    print("[%d/%d] mean_loss : %0.2f" % (
                        epoch, EPOCH, np.mean(losses)))
                    losses = []
        self.model = model