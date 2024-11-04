import json
import requests
from logging import Logger

def make_application_yml(HOST: str, PORT: str, PSW: str, LOGGER: Logger, LAVALINK_PLUGINS: dict) -> None:
    print()
    LOGGER.info("Creating application.yml file...")

    plugin_tags = {}
    for key, value in LAVALINK_PLUGINS.items():
        plugin_json = json.loads(requests.get(value).text)
        for i in plugin_json:
            if not i.get('prerelease'):
                plugin_tags[key] = i['tag_name']
                break

    plugin_str = ""
    for key, value in plugin_tags.items():
        plugin_str += f"    - dependency: \"{key}:{value}\"\n"
        plugin_str += "      snapshot: false\n"
    
    print(plugin_str)
    print()

    f = open("application.yml", 'w')
    f.write(f"""server: # REST and WS server
  port: {PORT}
  address: {HOST}
http2:
    enabled: false # Whether to enable HTTP/2 support
plugins:
  youtube:
    enabled: true # Whether this source can be used.
    allowSearch: true # Whether "ytsearch:" and "ytmsearch:" can be used.
    allowDirectVideoIds: true # Whether just video IDs can match. If false, only complete URLs will be loaded.
    allowDirectPlaylistIds: true # Whether just playlist IDs can match. If false, only complete URLs will be loaded.
    # The clients to use for track loading. See below for a list of valid clients.
    # Clients are queried in the order they are given (so the first client is queried first and so on...)
    clients:
      - MUSIC
      - WEB
      - WEBEMBEDDED
      - ANDROID_MUSIC
      - TVHTML5EMBEDDED
      - IOS
      - MEDIA_CONNECT
    # You can configure individual clients with the following.
    # Any options or clients left unspecified will use their default values,
    # which enables everything for all clients.
    WEB: # names are specified as they are written below under "Available Clients".
      # This will disable using the WEB client for video playback.
      playback: false
    TVHTML5EMBEDDED:
      # The below config disables everything except playback for this client.
      playlistLoading: false # Disables loading of playlists and mixes for this client.
      videoLoading: false # Disables loading of videos for this client (playback is still allowed).
      searching: false # Disables the ability to search for videos for this client.

lavalink:
  plugins:
#    - dependency: "group:artifact:version"
#      repository: "repository"

{plugin_str}

  pluginsDir: "./plugins"
  server:
    password: "{PSW}"
    sources:
      # The default Youtube source is now deprecated and won't receive further updates. Please use https://github.com/lavalink-devs/youtube-source#plugin instead.
      youtube: false
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      nico: true
      http: true # warning: keeping HTTP enabled without a proxy configured could expose your server's IP address.
      local: false
    filters: # 모든 필터는 기본적으로 활성화되어 있습니다
      volume: true
      equalizer: true
      karaoke: true
      timescale: true
      tremolo: true
      vibrato: true
      distortion: true
      rotation: true
      channelMix: true
      lowPass: true
    bufferDurationMs: 400 # NAS 버퍼의 지속 시간. 값이 높을수록 더 긴 GC 일시 중지에 대해 더 잘 처리됩니다. JDA-NAS를 비활성화하려면 Duration <= 0입니다. 최소 40ms, 값이 낮을수록 일시 중지가 발생할 수 있습니다.
    frameBufferDurationMs: 5000 # 버퍼링할 오디오 시간(밀리초)
    opusEncodingQuality: 10 # Opus 인코더 품질. 유효한 값의 범위는 0에서 10까지입니다. 여기서 10은 최상의 품질이지만 CPU를 가장 많이 사용합니다.
    resamplingQuality: HIGH # 리샘플링 작업의 품질. 유효한 값은 LOW, MEDIUM 및 HIGH입니다. 여기서 HIGH는 CPU를 가장 많이 사용합니다.
    trackStuckThresholdMs: 10000 # 트랙이 멈출 수 있는 시간에 대한 임계값입니다. 오디오 데이터를 반환하지 않으면 트랙이 멈춥니다.
    useSeekGhosting: true # 탐색 고스팅은 탐색이 진행되는 동안 오디오 버퍼가 비워질 때까지 또는 탐색이 준비될 때까지 읽히는 효과입니다.
    youtubePlaylistLoadLimit: 6 # 각 100페이지의 페이지 수
    playerUpdateInterval: 5 # 플레이어 업데이트를 클라이언트에 보내는 빈도(초)
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    gc-warnings: true
    #ratelimit:
      #ipBlocks: ["1.0.0.0/8", "..."] # IP 차단 목록
      #excludedIps: ["...", "..."] # lavalink의 사용에서 명시적으로 제외되어야 하는 ip들
      #strategy: "RotateOnBan" # RotateOnBan | LoadBalance | NanoSwitch | RotatingNanoSwitch
      #searchTriggersFail: true # 429 코드가 발생하는 IP를 실패로 트리거해야 하는지 여부
      #retryLimit: -1 # -1 = 라바플레이어 기본값 | 0 = 무제한 | >0 = 재시도 최대값
    #youtubeConfig: # YouTube의 모든 연령 제한을 피하기 위해 필요하지만 일부 제한된 동영상은 연령 제한 없이도 재생할 수 있습니다.
      #email: "" # 구글 계정 이메일
      #password: "" # 구글 계정 비밀번호
    #httpConfig: # 악의적인 행위자가 음악 노드의 IP를 파악하여 공격하는 것을 차단하는 데 유용합니다. 이렇게 하면 http 프록시만 공격받게 됩니다.
      #proxyHost: "localhost" # 프록시의 호스트네임, (ip 또는 도메인)
      #proxyPort: 3128 # 프록시 포트, 3128 은 squidProxy 의 기본값입니다.
      #proxyUser: "" # 기본 인증 필드에 대한 선택적 사용자, 기본 인증을 사용하지 않는 경우 공백으로 두십시오.
      #proxyPassword: "" # 기본 인증을 위한 비밀번호

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

sentry:
  dsn: ""
  environment: ""
#  tags:
#    some_key: some_value
#    another_key: another_value

logging:
  file:
    path: ./logs/

  level:
    root: INFO
    lavalink: INFO

  request:
    enabled: true
    includeClientInfo: true
    includeHeaders: true
    includeQueryString: true
    includePayload: true
    maxPayloadLength: 10000


  logback:
    rollingpolicy:
      max-file-size: 1GB
      max-history: 30
""")

    f.close()

