import React from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';

export default class HomeScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null // setting header to null removes the header
    };
    render() {
        return (
            <View style={styles.container}>
                <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}> Rhythm </Text>
                <Button
                    title="Profile"
                    onPress={() => this.props.navigation.navigate('Profile')}
                />
            </View>
        );
    }
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#ffeceb',
        alignItems: 'center',
        justifyContent: 'center',
    },
});