'use strict';

var React = require('react-native');

var {
    StyleSheet,
} = React;

module.exports = StyleSheet.create({
    header: {
        flex: 1,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center',
    },
    container: {
        flex: 1,
        marginTop: 20,
        backgroundColor: '#ffeceb',
    },
    textHolder: {
        height: 200,
        alignItems: 'center'
    },
    footer: {
        height: 100,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center'
    },
    navButton: {
        height: 100,
        position: 'absolute', top: 0, bottom: 0, left: 0, right: 0,
        alignItems: 'center',
        justifyContent: 'center'
    },
    lineBreak: {
        borderBottomColor: 'black',
        borderBottomWidth: 1,
    },
    compositionContainer: {
        margin: 40
    },
    compositionItem: {
        height: 50,
    },
    inputContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
});