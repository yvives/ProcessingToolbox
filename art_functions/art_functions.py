import cupy as cp

def to_gpu(array, device=None, stream=None):
    """Copies the given CPU array to specified device.

    Args:
        array: Array to be sent to GPU.
        device: Device specifier.
        stream (cupy.cuda.Stream): CUDA stream. If not ``None``, the copy runs
            asynchronously.

    Returns:
        cupy.ndarray: Array on GPU.

        If ``array`` is already on GPU, then this function just returns
        ``array`` without performing any copy. Note that this function does not
        copy :class:`cupy.ndarray` into specified device.

    """
    check_cuda_available()
    with get_device(device):
        array_dev = get_device(array)
        if array_dev.id == cupy.cuda.device.get_device_id():
            return array

        if stream is not None:
            ret = cupy.empty_like(array)
            if array_dev.id == -1:
                # cpu to gpu
                src = array.copy(order='C')
                ret.set(src, stream)
            else:
                # gpu to gpu
                with array_dev:
                    src = array.copy()
                ret.data.copy_from_device_async(src.data, src.nbytes, stream)

            # to hold a reference until the end of the asynchronous memcpy
            stream.add_callback(lambda *x: None, (src, ret))
            return ret

        if array_dev.id == -1:
            return cupy.asarray(array)

        # Need to make a copy when an array is copied to another device
        return cupy.array(array, copy=True)
