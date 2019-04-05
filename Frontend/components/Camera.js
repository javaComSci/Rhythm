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

  render() {
    const { hasCameraPermission } = this.state;
    if (hasCameraPermission === null) {
      return <View />;
    } else if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    } else {
      return (
        <View style={{ flex: 1 }}>
          <Camera style={{ flex: 1 }} type={this.state.type}>
            <View
              style={{
                flex: 1,
                backgroundColor: 'transparent',
                flexDirection: 'row',
              }}>
              <TouchableOpacity
                style={{
                  flex: 0.1,
                  alignSelf: 'flex-end',
                  alignItems: 'center',
                }}
                onPress={() => {
                  this.setState({
                    type: this.state.type === Camera.Constants.Type.back
                      ? Camera.Constants.Type.front
                      : Camera.Constants.Type.back,
                  });
                }}>
                <Text
                  style={{ fontSize: 18, marginBottom: 10, color: 'white' }}>
                  {' '}Flip{' '}
                </Text>
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
