import React from 'react';
import { TextInput, FlatList, TouchableOpacity, Button, ScrollView, StyleSheet, Text, View } from 'react-native';

var styles = require('../style');

/*
requires integration with backend
*/

/* Register Screen */
// Screen shown to user to register an email, *and enter a code sent to their e-mail* ** => to-do

export default class RegisterScreen extends React.Component {
    static navigationOptions = {
        title: 'Welcome', header: null
    };
    render() {
        return (
            <View style={styles.container}>
            <View style={styles.header}>
              <Text style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                Register
              </Text>
              <View style={styles.lineBreak} />
            </View>
            <ScrollView>
              <View style={styles.inputContainer}>
                <View style={{alignItems: 'left', width: '90%'}}>
                  <Text
                    style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                    Email:
                  </Text>
                </View>
                <TextInput
                  style={{
                    width: '90%',
                    height: 40,
                    color: '#f19393',
                    borderColor: '#f19393',
                    borderWidth: 1,
                    fontWeight: 'bold',
                  }}
                  onChangeText={text => this.setState({ text })}
                  value={this.state.text}
                />
              </View>
            </ScrollView>
            <View style={styles.footer}>
              <TouchableOpacity
                onPress={() => this.props.navigation.navigate('Home')}
                style={styles.navButton}>
                <Text
                  style={{ color: '#f19393', fontWeight: 'bold', fontSize: 40 }}>
                  {' '}
                  Submit{' '}
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        );
    }
};
