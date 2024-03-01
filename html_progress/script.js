document.addEventListener("DOMContentLoaded", function () {
  fetchGrievanceStatusAndUpdateTimeline();
});

function fetchGrievanceStatusAndUpdateTimeline() {
  // Example API call
  //   fetch("https://your-api-endpoint.com/grievance/status")
  //     .then((response) => response.json())
  //     .then((data) => {
  //   const status = data.status; // Assuming the API returns an object with a status property
  updateTimeline("work-in-ground");
  // })
  // .catch((error) => console.error("Error fetching grievance status:", error));
}

function updateTimeline(currentStatus) {
  const registered = document.getElementById("registered");
  const ongoing = document.getElementById("ongoing");
  const workInProgress = document.getElementById("work-in-ground");
  const closed = document.getElementById("closed");

  if (currentStatus === "registered") {
    registered.classList.add("passed");
  } else if (currentStatus === "ongoing") {
    registered.classList.add("passed");
    ongoing.classList.add("passed");
  } else if (currentStatus === "work-in-ground") {
    registered.classList.add("passed");
    ongoing.classList.add("passed");
    workInProgress.classList.add("passed");
  } else if (currentStatus === "closed") {
    registered.classList.add("passed");
    ongoing.classList.add("passed");
    workInProgress.classList.add("passed");
    closed.classList.add("passed");
  }
}
