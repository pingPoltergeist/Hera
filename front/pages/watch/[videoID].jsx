import {addToWatchlist, getVideoByID} from "../../helpers/helperApiCalls"
import styles from "../../styles/components/Player.module.scss"
import ReactPlayer from "react-player"
import PlayerControls from "../../components/utils/PlayerControls";
import {useState, useRef} from "react";
import screenfull from "screenfull";
import {backend} from "../../backend";
import {withAuth} from "../../helpers/utilities";
import {getCookieToken, isAuthenticated} from "../../helpers/authApiCalls";
import Fallback from "../../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";
import {error} from "next/dist/build/output/log";

export async function getServerSideProps({ query, req, res }) {

    const token = getCookieToken(req, res)

    return getVideoByID(query.videoID, token).then(video => {
        if (!video) {
            return {
                notFound: true,
            }
        }
        return {props: {video}}
    })
}

const format = (seconds) => {
    if (isNaN(seconds)) {
        return '00:00'
    }

    const date = new Date(seconds * 1000)
    const hh = date.getUTCHours()
    const mm = date.getUTCMinutes()
    const ss = date.getUTCSeconds().toString().padStart(2,"0")

    if (hh) {
        return `${hh}:${mm.toString().padStart(2, "0")}:${ss}`
    }

    return `${mm}:${ss}`
}

let count = 0

const player = ({video}) => {

    const [control, setControl] = useState({
        playing: true,
        muted: false,
        volume: 0.75,
        played: 0,
        seeking: false,
        buffering: false
    })

    const token = isAuthenticated()

    const playerRef = useRef(null)
    const playerContainerRef = useRef(null)
    const controlsRef = useRef(null)


    const handleMouseMove = () => {
        controlsRef.current.style.visibility = "visible"
        document.body.style.cursor = "default"
        count = 0
    }

    const handlePlayPause = () => {
        setControl({ ...control, playing: !control.playing })
    }

    const handleRewind = () => {
        playerRef.current.seekTo(playerRef.current.getCurrentTime() - 10)
    }

    const handleForward = () => {
        playerRef.current.seekTo(playerRef.current.getCurrentTime() + 10)
    }

    const handleMute = () => {
        setControl({...control, muted: !control.muted, volume: 0})
    }

    const handleVolumeChange = (event, newValue) => {
        setControl({
            ...control,
            volume: parseFloat(newValue/100),
            muted: !newValue
        })
    }

    const handleVolumeSeekUp = (event, newValue) => {
        setControl({
            ...control,
            volume: parseFloat(newValue/100),
            muted: !newValue
        })
    }

    const toggleFullScreen = () => {
        screenfull.toggle(playerContainerRef.current)
    }

    const handleProgress = (playedSeconds) => {

        if (count > 1) {
            controlsRef.current.style.visibility = "hidden"
            document.body.style.cursor = "none"
            count = 0
        }

        if (controlsRef.current.style.visibility == "visible") {
            count += 1
        }

        if (!control.seeking) {
            setControl({...control, played: playedSeconds.played})
        }
    }

    const handleWatchList = (seconds) => {
        addToWatchlist(token, video.tmdb_id, seconds).then(response => {return null})
    }

    const handleSeek = (event, newValue) => {
        setControl({...control, played: parseFloat(newValue/100)})
    }

    const handleSeekMouseDown = (event) => {
        setControl({...control, seeking: true})
    }

    const handleSeekMouseUp = (event, newValue) => {
        setControl({...control, seeking: false})
        playerRef.current.seekTo(newValue / 100)
    }

    const handleBuffer = () => {
        setControl({...control, buffering: true})
    }

    const handleBufferEnd = () => {
        setControl({...control, buffering: false})
    }

    const handleError = (err) => {
        throw new Error("Error Occurred playing the video")
    }


    const currentTime = playerRef.current ? playerRef.current.getCurrentTime() : '00:00'
    const duration = playerRef.current ? playerRef.current.getDuration() : '00:00'

    const elapsedTime = format(currentTime)
    const totalDuration = format(duration)

    return (
            <div ref={playerContainerRef} onMouseMove={handleMouseMove} className={styles.player_container}>
                <ErrorBoundary FallbackComponent={Fallback}>
                    <ReactPlayer
                        onStart={() => {
                            screenfull.request()
                            if (video.timestamp) {
                                playerRef.current.seekTo(video.timestamp)
                            }
                        }}
                        onProgress={playedSeconds => {
                            handleProgress(playedSeconds)
                            handleWatchList(playedSeconds.playedSeconds)
                        }}
                        onBuffer={handleBuffer}
                        onBufferEnd={handleBufferEnd}
                        onError={handleError}
                        volume={control.volume}
                        muted={control.muted}
                        ref={playerRef}
                        playing={control.playing}
                        url={encodeURI(`${backend}${video.location}`)}
                        className={styles.main_player}
                        width="100%"
                        height="100%"
                    />
                </ErrorBoundary>
                <PlayerControls
                    ref={controlsRef}
                    onPlayPause={handlePlayPause}
                    playing={control.playing}
                    onRewind={handleRewind}
                    onForward={handleForward}
                    muted={control.muted}
                    onMute={handleMute}
                    onvolumechange={handleVolumeChange}
                    onVolumeSeekUp={handleVolumeSeekUp}
                    volume={control.volume}
                    onToggleFullScreen={toggleFullScreen}
                    played={control.played}
                    onSeek={handleSeek}
                    onSeekMouseDown={handleSeekMouseDown}
                    onSeekMouseUp={handleSeekMouseUp}
                    elapsedTime={elapsedTime}
                    totalDuration={totalDuration}
                    buffering={control.buffering}
                    video={video}/>
            </div>
    )
}

export default withAuth(player)