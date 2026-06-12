// DB
let scheduledDowntimes = [];
let argoApplications = [{ application_name: "myApp", syncStatus: "not synced" }];

// APIs mocks

const scheduleDowntime = () => {
  const downtimeId = Math.random();
  scheduledDowntimes.push(downtimeId);
  return downtimeId;
};

const cancelDowntime = (downtimeId) => {
  scheduledDowntimes = scheduledDowntimes.filter((item) => item !== downtimeId);
};

const argoCDSync = (application_name) => {
  argoApp = argoApplications.find((item) => item.application_name == application_name);
  // simulate some sync waiting
  if (argoApp) {
    argoApp.syncStatus = "sync";
  } else {
    throw `Application ${application_name} not found.`;
  }
};

const getAppSyncStatus = (application_name) => {
  argoApp = argoApplications.find((item) => item.application_name == application_name);
  return { status: argoApp.syncStatus, message: argoApp.message };
};

// get application_name from CLI
application_name = process.argv[2];

// check if any datadog downtime related to the application is present
// GET all downtimes
// If downtime already exists, fetch it. Else create it
let downtime_already_exists = false; // not implemented
let downtime_id;
if (downtime_already_exists) {
  //   downtime_id = getDowntime(); // not implemented
  console.log("downtime already exists");
} else {
  downtime_id = scheduleDowntime();
  console.log("downtime has been created");
}

// Downtime is enabled

// trigger app sync
// sync application
argoCDSync(application_name);
// check if application is synced
app_not_synced = false;
while (app_not_synced) {
  sync_status = getAppSyncStatus(application_name);
  app_not_synced = syncStatus == "not synced";
  if (app_not_synced) {
    console.log(syncStatus.message);
  }
}

console.log("app is synced");

// If downtime already existed at the beginning, do not remove the downtime
// else, remove the one that has been created
cancelDowntime(downtime_id);
console.log("downtime cancelled");
