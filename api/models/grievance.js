const mongoose = require("mongoose");

const Comment = require("./comment");

const grievanceSchema = new mongoose.Schema(
  {
    audio: { type: String},
    transcript: { type: String },
    subjectContentText: { type: String },
    code: { type: Number },
    categoryName: { type: String },
    label: { type: String },
    status: { type: String },
    comments: [Comment.schema]
  },
  { timestamps: true }
);

const Grievance = mongoose.model("Grievance", grievanceSchema);

module.exports = Grievance;
