self.addEventListener('push', event => {
    const data = event.data;
    self.registration.showNotification('WhoWhyWhen', {
        body: data.text(),
        icon: '/logo.png'
    });
});
