import {EnqueueSnackbar} from 'notistack';

export let NotificationManager: EnqueueSnackbar;

export function setNotificationManager(enqueueSnackbar: EnqueueSnackbar): void {
  NotificationManager = enqueueSnackbar;
}
