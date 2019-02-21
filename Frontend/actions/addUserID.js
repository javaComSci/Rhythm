const ADD_USERID = 'ADD_USERID'

/*
ADD_EMAIL Action to add an email to the store
*/

export function addUserID(id) {
    return {
        type: 'ADD_USERID',
        id: id,
    }
};