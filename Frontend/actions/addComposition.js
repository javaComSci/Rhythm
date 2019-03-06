const ADD_COMPOSITION = 'ADD_COMPOSITION'

/*
ADD_COMPOSITION Action to add a composition to the store
*/

export function addComposition(composition) {
    return {
        type: 'ADD_COMPOSITION',
        composition: composition,
    }
};