const ADD_EMAIL = 'ADD_EMAIL'

/*
ADD_EMAIL Action to add an email to the store
*/

export function addEmail(email) {
    return {
        type: 'ADD_EMAIL',
        email: email,
    }
};