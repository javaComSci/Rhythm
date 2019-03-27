import React from 'react';
import { Text, View, ActivityIndicator } from 'react-native';
import { connect } from 'react-redux';

var styles = require('../style');


class SelectMusicScreen extends React.Component {
    render() {
        return (
            <View style={styles.header}>
            	<Text> PIANO!!! </Text>
            </View>
        )
    }
}

export default SelectMusicScreen;