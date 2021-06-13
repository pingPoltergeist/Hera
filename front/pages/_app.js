import 'swiper/swiper.scss';
import 'swiper/swiper-bundle.css';
import '../styles/global/globals.scss'
import Base from '../components/Base'
import '/styles/global/utils/nprogress.scss'

import store from '../store/store'
import { Provider } from 'react-redux'

function Hera({ Component, pageProps }) {


  return (
      <Provider store={store}>
          <Base>
            <Component {...pageProps}/>
          </Base>
      </Provider>
  )
}

export default Hera
