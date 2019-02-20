import React from 'react';
import { AppRegistry } from 'react-native';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import SheetCamera from './components/SheetCamera'
import { AppNavigator, middleware } from './navigators/AppNavigation'
import AppReducer from './reducers/AppReducer'


class RhythmApp extends React.Component {
  store = createStore(AppReducer, applyMiddleware(middleware));

  render() {
    return (
      <Provider store={this.store}>
        <AppNavigator />
      </Provider>
    )
  }
}

//AppRegistry.registerComponent('Rhythm', () => RhythmApp);

export default RhythmApp;
