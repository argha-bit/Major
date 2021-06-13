const bodyParser = require("body-parser");
const express = require("express");
const mongoose = require("mongoose");
const { uuid } = require("uuidv4");
const spawn = require("child_process").spawn;
const cors = require("cors");

//myFirstDatabase
mongoose.connect(
  "mongodb+srv://argha1234:1234@cluster0.qcavj.mongodb.net/QuickPeek?retryWrites=true&w=majority",
  { useUnifiedTopology: true, useNewUrlParser: true }
);

const newSchema = new mongoose.Schema(
  {
    _id: String,
    Name: String,
    Password: String,
    email: {
        type: String,
        unique: true 
      },
    dataRepo: [String],
    live: String
  },
  { collection: "Userdata" }
);
const newModel = mongoose.model("Userdata", newSchema);

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
const corsOptions = {
  origin: "*",
};
app.use(cors(corsOptions));

app.get("/", (req, res) => {
  res.send("Express Running");
});
app.get("/faces", (req, res) => {
  var process = spawn("python", ["./face_rec.py"]);
  res.header("Access-Control-Allow-Origin", "*");
  process.stdout.on("data", (data) =>
    res.status(200).json({ success: true, datas: data })
  );
});
app.post("/userinfo", (req, res, next) => {
  let Id = req.body.id;
  console.log(Id);
  res.header("Access-Control-Allow-Origin", "*");
  newModel.findOne({ _id: Id }, (err, resp) => {
    if (err) res.status(500).json("Internal Error!");
    if (!res) res.status(404).json("Not Found");
    else res.status(200).json(resp);
  });
});
app.post("/userdataupload", async (req, res, next) => {
  let id = uuid();
  console.log(id);
  console.log(req.body);
  res.header("Access-Control-Allow-Origin", "*");
  const upload = new newModel({
    _id: id,
    Name: req.body.name,
    Password: req.body.password,
    email: req.body.email,
    dataRepo: [],
    live:req.body.live
  });
  try {
    await upload.save();
    res.status(200).json({ Success: true, message: id });
  } catch (error) {
    res.status(400).json({ Success: false });
  }
});
app.post("/authenticate", (req, res, next) => {
  let email = req.body.email;
  let password = req.body.password;
  console.log(req.body);
  res.header("Access-Control-Allow-Origin", "*");

  newModel.findOne({ email: email, Password: password }, (err, user) => {
    if (err) {
      console.log(err);
      res
        .status(500)
        .json({ message: "Internal error! Please try Again later" });
    }
    if (!user) {
      res
        .status(404)
        .json({
          Success: "false",
          message: "User is not authenticated, Please Contact QuickPeek Team",
        });
    } else res.status(200).send(user);
  });
});
app.listen(8080, () => {
  console.log("App Started at 8080");
});
