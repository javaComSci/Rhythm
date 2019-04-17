import { PLACE_JSON } from './types';

export const placeJson = filejsoninfo => {
  return {
    type: PLACE_JSON,
    filejsoninfo: filejsoninfo,
  }
}
