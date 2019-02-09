import { createStackNavigator, createAppContainer } from "react-navigation";
import { connect } from 'react-redux';
import HomeScreen from './HomeScreen';
import ProfileScreen from './ProfileScreen';
import CompositionScreen from './CompositionScreen';
import React, { Component } from 'react';

/*
Create the stack navigator
*/
const AppNavigator = createStackNavigator(
  {
    Home: HomeScreen,
    Profile: ProfileScreen,
    Compositions: CompositionScreen
  },
  {
    initialRouteName: "Home"
  }
);

const MainApplication = createAppContainer(AppNavigator)

class AppNavigation extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <MainApplication screenProps={this.props} />
  }
}
state = {
  userEmail: '',
  userCompositions: []
} 


const mapStateToProps = state => {
  return {
    places: state.userCompositions.userCompositions
  }
}

const mapDispatchToProps = dispatch => {
  return {
    add: (name) => {
      dispatch(addComposition(name))
    }
  }
}
/*
Create the app container
*/
export default connect(mapStateToProps, mapDispatchToProps)(AppNavigation); // 