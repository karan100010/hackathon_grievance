const express = require("express");
const bodyParser = require("body-parser");
const multer = require("multer");
const mongoose = require("mongoose");
const { v4: uuidv4 } = require("uuid");
const path = require("path");

const grievanceRoutes = require("./routes/grievance");

const app = express();
const port = 8080;

// const fileStorage = multer.diskStorage({
//   destination: (req, file, cb) => {
//     cb(null, "audios");
//   },
//   filename: (req, file, cb) => {
//     cb(null, uuidv4() + ".mp3");
//   },
// });

app.use(bodyParser.json());
// app.use(multer({ storage: fileStorage }).single("audio"));

app.use("/grievance", grievanceRoutes);
// app.use("/audios", express.static(path.join(__dirname, "audios")));

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET, POST, PUT, PATCH, DELETE"
  );
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

app.use((error, req, res, next) => {
  console.log(error);
  const status = error.statusCode;
  const message = error.message;
  res.status(status).json({
    message: message,
  });
});

mongoose
  .connect(
    "mongodb+srv://root:toor@testcluster.exl8ah5.mongodb.net/Grievance?retryWrites=true&w=majority&appName=TestCluster"
  )
  .then((result) => {
    app.listen(port, () => {
      console.log(`Server running at port ${port}`);
    });
  })
  .catch((err) => console.log(err));
