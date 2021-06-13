import styles from "/styles/components/utils/PlayerControls.module.scss";
import {Button, CircularProgress, Grid, IconButton, Slider, Typography, withStyles} from "@material-ui/core";
import {
    FastForward,
    FastRewind,
    Fullscreen,
    PlayArrow,
    VolumeUp,
    Pause,
    VolumeOff,
    ArrowBack
} from "@material-ui/icons";
import {forwardRef} from "react";
import {useRouter} from "next/router";

const Seekbar = withStyles({
    root: {
        height: 8,
    },
    thumb: {
        height: 18,
        width: 18,
        backgroundColor: '#FF3D00',
        border: '2px solid currentColor',
        marginTop: -8,
        marginLeft: -12,
        '&:focus, &:hover, &$active': {
            boxShadow: 'inherit',
        },
    },
    active: {},
    valueLabel: {
        left: 'calc(-50% + 4px)',
    },
    track: {
        height: 2,
        borderRadius: 4,
    },
    rail: {
        height: 2,
        borderRadius: 4,
    },
})(Slider);

const PlayerControls = forwardRef(({
    video,
    onPlayPause,
    playing,
    onRewind,
    onForward,
    muted,
    onMute,
    onvolumechange,
    onVolumeSeekUp,
    volume,
    onToggleFullScreen,
    played,
    onSeek,
    onSeekMouseDown,
    onSeekMouseUp,
    elapsedTime,
    totalDuration,
    buffering
}, ref) => {

    const router = useRouter()

    return (
        <div ref={ref} className={styles.control_container}>

            { /*Top Section*/ }
            <Grid container direction={"row"} alignItems={"center"} className={styles.control_section}>
                <IconButton onClick={() => router.back()} aria-label="back"><ArrowBack fontSize={"inherit"}/></IconButton>
                <Grid item><p className={styles.video_title}>{video.name}</p></Grid>
            </Grid>

            { /*Middle Section*/ }
            <Grid container direction={"row"} alignItems={"center"} justify={"center"} className={styles.control_section}>
                <IconButton onClick={onRewind} className={styles.control_icons} aria-label="rewind"><FastRewind fontSize={"inherit"}/></IconButton>
                {buffering
                    ? <CircularProgress size={100} className={styles.control_icons}/>
                    : <IconButton onClick={onPlayPause} className={styles.control_icons} aria-label="play">{playing ? <Pause fontSize={"inherit"}/> : <PlayArrow fontSize={"inherit"}/>}</IconButton>
                }
                <IconButton onClick={onForward} className={styles.control_icons} aria-label="forward"><FastForward fontSize={"inherit"}/></IconButton>
            </Grid>

            { /*Bottom Section*/ }
            <Grid container direction={"row"} alignItems={"center"} justify={"space-between"} className={styles.control_section}>
                <Grid item xs={12}>
                    <Seekbar
                        min={0}
                        max={100}
                        value={played * 100}
                        onChange={onSeek}
                        onMouseDown={onSeekMouseDown}
                        onChangeCommitted={onSeekMouseUp}
                        defaultValue={20}
                    />
                </Grid>
                <div className={styles.bottom_control_container}>
                    <div className={styles.right_section}>
                        <IconButton onClick={onPlayPause} className={styles.bottom_control_icons} aria-label="play">{playing ? <Pause fontSize={"large"}/> : <PlayArrow fontSize={"large"}/>}</IconButton>
                        <IconButton onClick={onMute} className={styles.bottom_control_icons} aria-label="forward">{muted ? <VolumeOff fontSize={"large"} /> : <VolumeUp fontSize={"large"}/>}</IconButton>
                        <Slider onChangeCommitted={onVolumeSeekUp} onChange={onvolumechange} min={0} max={100} value={volume * 100}/>
                        <Button variant={"text"} style={{color: "white", marginLeft: 16}}>
                            <Typography>{elapsedTime}/{totalDuration}</Typography>
                        </Button>
                    </div>

                    <div className={styles.left_section}>
                        <IconButton onClick={onToggleFullScreen} className={styles.bottom_control_icons} aria-label="Full Screen"><Fullscreen fontSize={"large"}/></IconButton>
                    </div>
                </div>
            </Grid>
        </div>
    )
})

export default PlayerControls