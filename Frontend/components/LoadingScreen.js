import React from 'react';
import { Text, View, ActivityIndicator, Animated } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style');

// class LoadingScreen extends React.Component {
// 	state = {
// 		fadeAnim: new Animated.Value(0),
// 	}

// 	componentDidMount(){
// 		Animated.timing(
// 			this.state.fadeAnim,
// 			{
// 				toValue: 1,
// 				duration: 10000,
// 			}
// 		).start()
// 	}

// 	render(){
// 		let { fadeAnim } = this.state;

// 		 return (
// 		      <Animated.View                 // Special animatable View
// 		        style={{
// 		          ...this.props.style,
// 		          opacity: fadeAnim,         // Bind opacity to animated value
// 		        }}
// 		      >
// 		        {this.props.children}
// 		      </Animated.View>
// 		);
// 	}
// }

class LoadingScreen extends React.Component {
    render() {
        return (
            <View style={styles.header}>
                <ActivityIndicator size="large" color="#f19393" />
            </View>
        )
    }
}

export default LoadingScreen;