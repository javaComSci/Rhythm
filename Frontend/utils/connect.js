export default class Connection {
    static url = "http://18.237.79.152:5000"

    static connect(endpoint, method, body, flags, callback) {
        const request = {
            method: method,
            headers: {
                Accept: 'application/json',
                'ContentType': 'application/json',
                ...flags
            }
        }

        if (body != null) {
            request.body = JSON.stringify(body);
        }

        fetch(this.url + endpoint, request).then((response) => response.json())
            .then((responseJson) => {
                callback(responseJson);
            })
            .catch((error) => {
                console.error(error);
            })
    }
}