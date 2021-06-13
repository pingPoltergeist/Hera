import { Swiper, SwiperSlide } from 'swiper/react'
import SwiperCore, { Navigation } from 'swiper'
import styles from '/styles/components/utils/SeasonSlider.module.scss'
import Image from 'next/image'
import Link from "next/link"

SwiperCore.use([Navigation])

const SeasonSlider = ({ medias, title }) => {
    return (
        <div className={styles.slider_container}>
            {title && <p className={styles.slider_title}>{title}</p>}
            <Swiper spaceBetween={20} slidesPerView={3} className={styles.slider_body} navigation >
                {medias && medias.map((media, index) => (
                    <SwiperSlide className={styles.card} key={index}>
                        <Link href={`/watch/${media.tmdb_id}`}>
                            <div className={styles.card_content}>
                                {media.thumbnail && <Image layout="fill" src={media.thumbnail} objectFit={'cover'} className={styles.card_img}/>}
                                <h4 className={styles.card_name}>{media.name}</h4>
                            </div>
                        </Link>
                    </SwiperSlide>

                ))}
            </Swiper>
        </div>
    )
}

export default SeasonSlider