const Grievance = require("../models/grievance");

exports.getGrievances = (req, res, next) => {
  Grievance.find()
    .then((grievances) => {
      if (!grievances) {
        const error = new Error("Could not find grievance.");
        error.statusCode = 404;
        throw error;
      }

      res
        .status(200)
        .json({ message: "Fetched grievances successfully.", grievances: grievances });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

exports.getGrievance = (req, res, next) => {
  const grievanceId = req.params.grievanceId;

  Grievance.findById(grievanceId)
    .then((grievance) => {
      if (!grievance) {
        const error = new Error("Could not find grievance.");
        error.statusCode = 404;
        throw error;
      }

      res
        .status(200)
        .json({ message: "Grievance fetched.", grievance: grievance });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

exports.postGrievance = (req, res, next) => {
  // if (!req.file) {                                                                                                                     
  //   const error = new Error("No audio file provided.");
  //   error.statusCode = 422;
  //   throw error;
  // }

  console.log(req.body);
  const audio = req.body.audio || "";
  const transcript = req.body.transcript || "";
  const subjectContentText = req.body.subjectContentText || "";
  const code = req.body.code ? +req.body.code : 0;
  const categoryName = req.body.categoryName || "";
  const label = req.body.label || "";
  const status = "Open";

  // Create grievance in db
  const greivance = new Grievance({
    audio,
    transcript,
    subjectContentText,
    code,
    categoryName,
    label,
    status,
  });

  greivance
    .save()
    .then((result) => {
      res.status(201).json({
        message: "grievance added sucessfully!",
        greivance: result,
      });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};
exports.getAllGrievances = (req, res, next) => {
  Grievance.find()
    .then((grievances) => {
      res.status(200).json({
        message: "Grievances fetched.",
        grievances: grievances,
      });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

exports.getAllGrievancesbyCategoryName = (req, res, next) => {
  const categoryName = req.params.categoryName;
  Grievance.find({ categoryName: categoryName })
    .then((grievances) => {
      res.status(200).json({
        message: "Grievances fetched.",
        grievances: grievances,
      });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
}
exports.getAllGrievancesbyStatus = (req, res, next) => {
  const status = req.params.status;
  Grievance.find({ status: status })
    .then((grievances) => {
      res.status(200).json({
        message: "Grievances fetched.",
        grievances: grievances,
      });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
}

exports.updateStatus = (req, res, next) => {
  const postId = req.params.grievanceId;
  
  const status = req.body.status;
  
  Grievance.findById(postId)
    .then((result) => {
      // console.log(post);
      if (!result) {
        const error = new Error("Could not find post.");
        error.statusCode = 404;
        throw error;
      }
    
      result.status = status;

      return result.save();
    })
    .then((result) => {
      res.status(200).json({ message: "Status updated!", status: result.status });
    })
    .catch((err) => {
      if (!err.statusCode) {
        err.statusCode = 500;
      }
      next(err);
    });
};

