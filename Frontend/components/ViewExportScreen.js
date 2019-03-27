import React from 'react';
import { ListItem, Dimensions, TextInput, TouchableOpacity, ScrollView, StyleSheet, View, Text, KeyboardAvoidingView, Image, ImageBackground } from 'react-native';
// import { Header } from 'react-navigation';
import { connect } from 'react-redux';
import { Button, Header } from 'react-native-elements';
import PinchZoomView from 'react-native-pinch-zoom-view';

var styles = require('../style')
var background = require('../assets/backgroundImage.png')

class ViewExportScreen extends React.Component{

	constructor(props) {
		super(props);
		this.state = {
			sheet_ids: this.props.sheet_ids,
			email: this.props.email,
		}
	}

	static navigationOptions = {
    	title: 'Welcome', header: null
  	};

  	exportSheets = () => {
  		console.log("HERE")
  		console.log(this.state.sheet_ids)
  		console.log(this.state.email)
  		if (this.state.email != '') {
            // has entered email
            updateInfo = ['name'];
            updateInfo.push(this.state.nameText);
            fetch('http://18.237.79.152:5000/createPDF', {
                method: 'POST',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                },
            }).then((res) => {
                this.props.navigation.navigate('EditMusicScreen')
            }).catch((res) => {
                console.log("err", res)
            });
        }
  	}

	render() {

		return (
			  <ImageBackground style={{ width: '100%', height: '100%' }}>
	            <View style={styles.container}>
	                <View></View>
	                <View>
	                    <View style={styles.operatorContainer}>
	                        <TextInput style={{ height: 50, width: '80%', borderColor: 'gray', borderWidth: 1}}
	                        	onChangeText={(email) => this.setState({email})}
	 							value={this.state.email}/>
	                        <TouchableOpacity style={styles.openButton} onPress={() => this.exportSheets()}>
	                            <Text style={{ color: 'white', fontSize: 30 }}>Email PDF</Text>
	                        </TouchableOpacity>
	                    </View>
	                </View>
	            </View>
	        </ImageBackground>
		);
	}

}


	// <View>
	// 			<View style={styles.operatorContainer}>                            
	// 				<TextInput
	// 						style={{height: 40}}
	// 						onChangeText={(email) => this.setState({email})}
	// 						value={this.state.email}
	// 				/>

	// 				<Button
 //                            onPress={() => this.exportSheets()}
 //                            title="Email PDF Version"
 //                            style={styles.button}
 //                    />

	//             </View>	

	// 		</View>

export default ViewExportScreen

