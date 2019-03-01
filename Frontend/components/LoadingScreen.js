import React from 'react';
import { Text, View, ActivityIndicator } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style');

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