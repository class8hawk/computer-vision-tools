  elif args.loss_type==7:
    print("===>hk sv")
    s = args.margin_s
    m = args.margin_m
    assert s>0.0
    assert m>=0.0
    assert m<(math.pi/2)
    _weight = mx.symbol.L2Normalization(_weight, mode='instance')
    nembedding = mx.symbol.L2Normalization(embedding, mode='instance', name='fc1n')*s
    fc7 = mx.sym.FullyConnected(data=nembedding, weight = _weight, no_bias = True, num_hidden=args.num_classes, name='fc7')
    zy = mx.sym.pick(fc7, gt_label, axis=1)
    cos_t = zy/s
    cos_m = math.cos(m)
    sin_m = math.sin(m)
    mm = math.sin(math.pi-m)*m
    #threshold = 0.0
    threshold = math.cos(math.pi-m)
    if args.easy_margin:
      cond = mx.symbol.Activation(data=cos_t, act_type='relu')
    else:
      cond_v = cos_t - threshold
      cond = mx.symbol.Activation(data=cond_v, act_type='relu')
    body = cos_t*cos_t
    body = 1.0-body
    sin_t = mx.sym.sqrt(body)
    new_zy = cos_t*cos_m
    b = sin_t*sin_m
    new_zy = new_zy - b
    costhta=new_zy
    new_zy = new_zy*s
    if args.easy_margin:
      zy_keep = zy
    else:
      zy_keep = zy - s*mm
    new_zy = mx.sym.where(cond, new_zy, zy_keep)

    diff = new_zy - zy
    diff = mx.sym.expand_dims(diff, 1)
    gt_one_hot = mx.sym.one_hot(gt_label, depth = args.num_classes, on_value = 1.0, off_value = 0.0)
    inv_gt_one_hot=1-gt_one_hot
    body = mx.sym.broadcast_mul(gt_one_hot, diff)
    
    cosallx=fc7/s
    t=1.2
    h=s*(t-1)*(cosallx+1)
    costhta=mx.sym.expand_dims(costhta, 1)
    greatthany=mx.sym.broadcast_greater(cosallx,costhta)
    bodysv=greatthany*h*inv_gt_one_hot
    
    fc7 = fc7+body+bodysv