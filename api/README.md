Grievance API Documentation
Overview
This API allows you to add a grievance by submitting a form containing an audio file and related information. Use "npm i" to install the dependencies Use "npm start" to run the server

Base URL
All API requests should be made to: http://localhost:8080/

Endpoint
1. Add Grievance
Endpoint URL:
POST /grievance/post

Description:
This endpoint allows you to add a grievance by submitting a form containing an audio file and related information.

Parameters:
audioFile: (File) - The audio file containing the grievance audio.
transcript: (String) - The transcript of the audio file.
subjectContentText: (String) - The text content related to the subject of the grievance.
code: (Number) - A numerical code associated with the grievance.
categoryName: (String) - The category to which the grievance belongs.
label: (String) - A label associated with the grievance.
status: (String) - The status of the grievance.


Response Example:
{ "_id": "Unique Id", "status": "Open", "message": "Grievance added successfully", "audioUrl": "/audios/unique_grievance_id", "createdDate": "2024-02-25T12:00:00Z", "updatedDate": "2024-02-25T12:00:00Z", "transcript": "Example transcript", "subjectContentText": "Example subject content", "code": 123, "categoryName": "ExampleCategory", "label": "ExampleLabel", }


EndPoint
1. Get Grievance
Endpoint URL
GET /grievance/check-status/:grievanceId


