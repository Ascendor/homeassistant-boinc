"""Boinc Remote class wrapping boinc_client as RemoteEntity."""

from _collections_abc import Iterable
from boinc_client import Boinc
from boinc_client.clients.rpc_client import RpcClient

from homeassistant.components.remote import RemoteEntity


class BoincRemote(RemoteEntity):
    """Boinc Remote class wrapping boinc_client as RemoteEntity."""

    def __init__(self, host, name, port, api_key, logger) -> None:
        """__init__ takes Hostname, Port and API-Key of the to-be-controlled BOINC PC, plus a free name and a logger."""
        # Hostname or IP of the running BOINC client
        self.host = host
        self._name = name
        self.port = port
        self.api_key = api_key
        self.logger = logger
        # Create an RPC client to connect to the BOINC socket
        self.boinc_client = self.create_boinc_client()

    def create_boinc_client(self):
        boinc_client =  None
        try:
            rpc_client = RpcClient(hostname=self.host, port=self.port, password=self.api_key)
            rpc_client.authenticate()
            boinc_client = Boinc(rpc_client=rpc_client)
        except ConnectionError as conn_ex:
            self.logger.error(f"Failed to connect to Boinc: {conn_ex}")
        except Exception as e:
            self.logger.error(f"Something went really wrong with Boinc: {e}")
        return boinc_client

    def reconnect_client(self):
        self.logger.info("Recycling RPC client")
        self.boinc_client = self.create_boinc_client()


    async def async_turn_off(self, activity: str = "None", **kwargs):
        """Send the power on command."""
        try:
            clientstate = self.boinc_client.set_cpu_run_mode("never")
            self.logger.info(clientstate)
        except Exception as e:
            self.logger.warning(e)
            self._attr_is_on = False
            self.reconnect_client()

    async def async_turn_on(self, activity: str = "None", **kwargs):
        """Send the power on command."""
        clientstate = self.boinc_client.set_cpu_run_mode("always")
        self.logger.info(clientstate)

    async def async_update(self):
        """Update state."""
        try:
            clientstate = self.boinc_client.get_cc_status()
            self.logger.info(clientstate)
            self._attr_is_on = clientstate["cc_status"]["task_mode"] == 1
        except Exception as e:
            self.logger.warning(e)
            self._attr_is_on = False
            self.reconnect_client()

    async def async_send_command(self, command: Iterable[str], **kwargs):
        """Send commands to a device."""
        for each_command in command:
            match each_command:
                case "cpu_100":
                    try:
                        #clientstate = self.boinc_client.set_cpu_usage_limit("100")
                        clientstate = self.boinc_client.update_global_prefs_override({"cpu_usage_limit": 100.0})
                        clientstate = self.boinc_client.read_global_prefs_override();
                        self.logger.info(clientstate)
                    except Exception as e:
                        self.logger.warning(e)
                        self._attr_is_on = False
                        self.reconnect_client()
                case "cpu_50":
                    try:
                        clientstate = self.boinc_client.update_global_prefs_override({"cpu_usage_limit": 50.0})
                        clientstate = self.boinc_client.read_global_prefs_override();
                        self.logger.info(clientstate)
                    except Exception as e:
                        self.logger.warning(e)
                        self._attr_is_on = False
                        self.reconnect_client()
                case "cpu_25":
                    try:
                        clientstate = self.boinc_client.update_global_prefs_override({"cpu_usage_limit": 25.0})
                        clientstate = self.boinc_client.read_global_prefs_override();
                        self.logger.info(clientstate)
                    except Exception as e:
                        self.logger.warning(e)
                        self._attr_is_on = False
                        self.reconnect_client()
                case "cpu_0":
                    try:
                        clientstate = self.boinc_client.update_global_prefs_override({"cpu_usage_limit": 0.01})
                        clientstate = self.boinc_client.read_global_prefs_override();
                        self.logger.info(clientstate)
                    except Exception as e:
                        self.logger.warning(e)
                        self._attr_is_on = False
                        self.reconnect_client()


    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self._attr_is_on
