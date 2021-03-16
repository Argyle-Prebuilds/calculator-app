import {store} from 'react-notifications-component';

export const displayErrorNotifications = (error, ignoreKeys = []) => {
  if (error.response !== undefined) {
    const errors = error.response.data;
    if (typeof errors === "string")
      return renderNotification('Something went wrong.', 'error');

    for (let key of Object.keys(errors)) {
      if (ignoreKeys.includes(key)) continue;
      if (Array.isArray(errors[key])) {
        for (let element of errors[key]) {
          renderNotification(element, 'error')
        }
        continue;
      }
      renderNotification(errors[key], 'error')
    }
  } else {
    renderNotification('Something went wrong.', 'error')
  }
};

export const renderNotification = (message, type = 'success') => {
  store.addNotification({
    title: type === 'success' ? 'Success' : 'Error',
    message: message,
    type: type === 'success' ? 'success' : 'danger',
    insert: "top",
    container: "top-right",
    animationIn: ["animate__animated", "animate__fadeIn"],
    animationOut: ["animate__animated", "animate__fadeOut"],
    dismiss: {
      duration: 5000,
      onScreen: true
    }
  });
}
