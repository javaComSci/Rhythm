const ADD_TARGET = 'ADD_TARGET'

/*
ADD_EMAIL Action to add an email to the store
*/

export function addTarget(target) {
    return {
        type: ADD_TARGET,
        target: target,
    }
};