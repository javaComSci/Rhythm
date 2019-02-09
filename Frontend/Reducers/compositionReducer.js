import { ADD_COMPOSITION } from '../Actions/types';

const initialState = {
    userEmail: '',
    userCompositions: []
}

const compositionReducer = (state = initialState, action) => {
    switch (action.type) {
        case ADD_COMPOSITION:
            return {
                ...state,
                userCompositions: state.compositions.concat({
                    key: Math.random(),
                    value: action.payload
                })
            };
        default:
            return state;
    }
}

export default compositionReducer;