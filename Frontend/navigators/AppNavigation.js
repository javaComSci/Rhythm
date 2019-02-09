import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { createStackNavigator } from 'react-navigation';
import {
  reduxifyNavigator,
  createReactNavigationReduxMiddleware,
} from 'react-navigation-redux-helpers';

import HomeScreen from '../HomeScreen';
import ProfileScreen from '../ProfileScreen';
import CompositionScreen from '../CompositionScreen';

const middleware = createReactNavigationReduxMiddleware(
  'root',
  state => state.nav
)

const RootNavigator = createStackNavigator({
  Home: { screen: HomeScreen },
  Profile: { screen: ProfileScreen },
  Composition: { screen: CompositionScreen }
});

const AppWithNavigationState = reduxifyNavigator(RootNavigator, 'root');

const mapStateToProps = state => ({
  state: state.nav,
});

const AppNavigator = connect(mapStateToProps)(AppWithNavigationState);

export { RootNavigator, AppNavigator, middleware };