import { combineReducers } from 'redux';
import { NavigationActions } from 'react-navigation';
import { RootNavigator } from '../navigators/AppNavigation';

const homeAction = RootNavigator.router.getActionForPathAndParams('Home');
const initialNavState = RootNavigator.router.getStateForAction(
    homeAction,
    initialNavState
);

function nav(state = initialNavState, action) {
    let nextState;
    //console.log(action); //debug
    switch (action.type) {
        case 'ADD_EMAIL':
            return {
                ...state, isRegistered: action.email
            };
        case 'ADD_USERID':
            return {
                ...state, id: action.id
            };
        default:
            nextState = RootNavigator.router.getStateForAction(action, state);
            break;
    }

    return nextState || state;
}

const initalRegisterState = { isRegistered: false, id: "26342", compositions: [], target: [], };

function containsComp(obj, list) {
    for (var i = 0; i < list.length; i++) {
        if (list[i].key == obj.key)
            return true;
    }
    return false;
}

function auth(state = initalRegisterState, action) {
    console.log("ACTION")
    console.log(action)
    console.log("STATE")
    console.log(state)
    console.log("FIlE JSON INFO!!")
    switch (action.type) {
        case 'ADD_EMAIL':
            return { ...state, isRegistered: action.email }; //duplicate
        case 'ADD_USERID':
            console.log('user id route auth')
            return { ...state, id: action.id }
        case 'ADD_COMPOSITION':
            if (!containsComp(action.composition, state.compositions))
                return {
                    ...state, compositions: [...state.compositions, action.composition]
                };
        case 'ADD_TARGET':
                return {
                    ...state, target: [action.target]
                }
        case 'PLACE_JSON':
                return { ...state, file: action.filejsoninfo };
        default:
            return state;
    }
}

const AppReducer = combineReducers({
    nav,
    auth
});

export default AppReducer;
