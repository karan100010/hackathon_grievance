const express = require('express');

const grievanceController = require('../controllers/grievance');

const router = express.Router();

router.get('/fetch-all', grievanceController.getGrievances);

router.get('/check-status/:grievanceId', grievanceController.getGrievance);

router.post('/post', grievanceController.postGrievance);

router.put('/update-status/:grievanceId', grievanceController.updateStatus);
router.get('/get-all', grievanceController.getAllGrievances);
router.get('/get-all/:categoryName', grievanceController.getAllGrievancesbyCategoryName);
router.get('/get-all/:status', grievanceController.getAllGrievancesbyStatus);

module.exports = router;
