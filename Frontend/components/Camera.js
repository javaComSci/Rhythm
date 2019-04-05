import React from 'react';
import { Text, View, TouchableOpacity, Dimensions } from 'react-native';
import { Camera, Permissions } from 'expo';
  // import { Header } from 'react-navigation';
  import { connect } from 'react-redux';
  import { Button, Header } from 'react-native-elements';
  import { Col, Row, Grid } from "react-native-easy-grid";
  import Icon from 'react-native-vector-icons/AntDesign'
  import PinchZoomView from 'react-native-pinch-zoom-view';


  import { Svg } from 'expo';
  const { Circle, Rect, Path, Line, G, Defs, Use } = Svg;
  const SCREEN_WIDTH = Dimensions.get('window').width
  const SCREEN_HEIGHT = Dimensions.get('window').height

export default class CameraExample extends React.Component {
  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
  };

  async componentDidMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }

  async snapPhoto() {       
    console.log('Button Pressed');
    if (this.camera) {
       console.log('Taking photo');
       const options = { quality: 1, base64: true, fixOrientation: true, 
       exif: true};
       await this.camera.takePictureAsync(options).then(photo => {
          photo.exif.Orientation = 1;            
           console.log(photo);  
           console.log("I TOOOK A PHOTO!!!")          
           });     
     }
  }

  render() {
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else {
      return (
        <View style={{ flex: 1 }}>
          <Camera style={{ flex: 1 }} type={this.state.type} ref={ (ref) => {this.camera = ref} }>
            <View
              style={{
                flex: 1,
                backgroundColor: 'transparent',
                flexDirection: 'row',
              }}>
              <TouchableOpacity style={{
                  position: "absolute",
                  top: '80%',
                  right: '44%',
                  alignItems: 'center',
                }}
                onPress={this.snapPhoto.bind(this)}>
                <Image style={{width: 50, height: 50}} source={require('../assets/capture.png')}          
                />
              </TouchableOpacity>
              <Svg height="100%"  width="100%">
                <Rect x={SCREEN_WIDTH/9} y={SCREEN_HEIGHT/10} width={SCREEN_WIDTH - SCREEN_WIDTH/9 - SCREEN_WIDTH/9} height={SCREEN_HEIGHT - SCREEN_HEIGHT/10 - (2 * SCREEN_HEIGHT/10)} fill="orange" strokeWidth="2" stroke="orange" strokeOpacity=".8" fillOpacity="0" />
                <Rect x={0} y={0} width={SCREEN_WIDTH/9} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH/9} y={0} width={SCREEN_WIDTH} height={SCREEN_HEIGHT/10} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH - SCREEN_WIDTH/9} y={SCREEN_HEIGHT/10} width={SCREEN_WIDTH} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="orange" strokeOpacity=".6" fillOpacity=".2" />
                <Rect x={SCREEN_WIDTH/9} y={SCREEN_HEIGHT - SCREEN_HEIGHT/10 - (1 * SCREEN_HEIGHT/10)} width={SCREEN_WIDTH- 2*SCREEN_WIDTH/9} height={SCREEN_HEIGHT} fill="orange" strokeWidth="0" stroke="green" strokeOpacity=".6" fillOpacity=".2" />
              </Svg>
            </View>
          </Camera>
        </View>
      );
    }
  }
}
